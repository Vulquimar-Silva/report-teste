import os
import sys
from flask import Flask, jsonify, request
from flask_migrate import Migrate

# Ajuste do PYTHONPATH, se necessário
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.core.config import config
from src.core.database import db
from src.core.logger import logger
from src.core.scheduler import schedule_tasks, run_etl_job, run_pdf_generation
from src.core.security import token_required
from src.models.user import User
from src.api.endpoints.dns_data_endpoint import dns_data_bp
from src.api.endpoints.internal_report import internal_report_bp
from src.api.endpoints.akamai_integration import akamai_bp


def create_app():
    """Cria e configura o aplicativo Flask."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # Inicializa o banco de dados + migrations
    db.init_app(app)
    Migrate(app, db)

    # Registra Blueprints
    app.register_blueprint(dns_data_bp, url_prefix='/api/dns')
    app.register_blueprint(internal_report_bp, url_prefix='/api/internal')
    app.register_blueprint(akamai_bp, url_prefix='/api/akamai')

    # Inicia o Scheduler (APScheduler) com o contexto da app
    schedule_tasks(app)

    logger.info("Aplicação Flask configurada com sucesso.")
    return app


app = create_app()


@app.route('/health', methods=['GET'])
def health_check():
    """Verifica a saúde da aplicação."""
    return jsonify({
        "status": "ok",
        "api_type": config.API_TYPE,
        "api_endpoint": config.API_ENDPOINT
    }), 200


@app.route('/token', methods=['POST'])
def get_token():
    """Gera um token JWT para autenticação."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Campos obrigatórios ausentes para gerar token.")
            return jsonify({'message': 'Username e password são obrigatórios!'}), 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            from src.core.security import generate_token
            token = generate_token(user.id)
            logger.info(f"Token gerado com sucesso para o usuário '{username}'.")
            return jsonify({'token': token}), 200

        logger.warning(f"Tentativa de login inválida para o usuário '{username}'.")
        return jsonify({'message': 'Credenciais inválidas!'}), 401

    except Exception as e:
        logger.error(f"Erro ao gerar token: {e}")
        return jsonify({'message': 'Erro ao processar a requisição.', 'error': str(e)}), 500


@app.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário no sistema."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Tentativa de registro sem username ou password.")
            return jsonify({'message': 'Username e password são obrigatórios!'}), 400

        if User.query.filter_by(username=username).first():
            logger.warning(f"Falha: o username '{username}' já existe.")
            return jsonify({'message': 'Username já existe!'}), 400

        new_user = User(username=username)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Novo usuário '{username}' registrado com sucesso.")
        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {e}")
        return jsonify({'message': 'Erro ao processar a requisição.', 'error': str(e)}), 500


@app.route('/run_pipeline', methods=['POST'])
@token_required
def run_pipeline(current_user=None):
    """
    Executa manualmente o pipeline (ETL + geração de PDFs).
    Caso REQUIRES_AUTH=False, current_user será None.
    Não envia e-mails, apenas gera e armazena no Google Drive.
    """
    user_id = current_user.id if current_user else 'Anônimo'
    logger.info(f"Usuário ID {user_id} solicitou execução do pipeline (ETL + PDF).")

    transformed_data = run_etl_job(app)

    # Se a função ETL retornou None, significa que houve erro no processo
    if transformed_data is None:
        logger.warning("ETL não retornou dados (None), encerrando pipeline.")
        return jsonify({"message": "ETL completed but returned None."}), 200

    # Se for um DataFrame vazio, .empty == True
    if hasattr(transformed_data, 'empty') and transformed_data.empty:
        logger.warning("ETL retornou DataFrame vazio, encerrando pipeline.")
        return jsonify({"message": "ETL completed but no data was transformed."}), 200

    run_pdf_generation(app, transformed_data)
    return jsonify({"message": "Pipeline (ETL + PDF) executado com sucesso."}), 200


if __name__ == "__main__":
    logger.info("Iniciando aplicação Flask em modo standalone...")
    app.run(host='0.0.0.0', port=5000)
