from flask import Flask, jsonify, request
from flask_migrate import Migrate
from src.core.scheduler import schedule_tasks
from src.api.endpoints.dns_data_endpoint import dns_data_bp
from src.api.endpoints.internal_report import internal_report_bp
from src.api.endpoints.akamai_integration import akamai_bp
from src.core.security import generate_token, token_required
from src.models.user import db, User
from src.core.config import config
from src.api.services.data_transformer import DataTransformer
from src.api.services.data_collector import DataCollector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Registra os Blueprints
app.register_blueprint(dns_data_bp, url_prefix='/api')
app.register_blueprint(internal_report_bp, url_prefix='/api/internal')
app.register_blueprint(akamai_bp, url_prefix='/api/akamai')

@app.route('/token', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists!'}), 400

    new_user = User(username=username)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/run_etl', methods=['POST'])
@token_required
def run_etl(current_user):
    data_collector = DataCollector()
    raw_data = data_collector.collect_dns_data()

    data_transformer = DataTransformer(app.config['SQLALCHEMY_DATABASE_URI'])
    transformed_data = data_transformer.transform_and_load(raw_data)

    return jsonify({"message": "ETL process completed successfully", "transformed_data": transformed_data}), 200

if __name__ == "__main__":
    schedule_tasks()
    app.run(host='0.0.0.0', port=5000)
