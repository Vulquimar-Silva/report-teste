from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DNSData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    requests = db.Column(db.Integer, nullable=False)
    blocked = db.Column(db.Integer, nullable=False)
    threat_level = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
