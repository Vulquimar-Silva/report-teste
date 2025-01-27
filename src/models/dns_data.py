from src.core.database import db
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from datetime import datetime

class DNSData(db.Model):
    __tablename__ = 'dns_data'
    __table_args__ = (
        UniqueConstraint('company_id', 'domain', name='unique_company_domain'),
    )

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    domain = db.Column(db.String(255), nullable=False)
    requests = db.Column(db.Integer, nullable=False, default=0)
    blocks = db.Column(db.Integer, nullable=False, default=0)
    threat_level = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    @validates('domain')
    def validate_domain(self, key, value):
        """Valida o domínio antes de salvar no banco de dados."""
        if not isinstance(value, str) or len(value) > 255:
            raise ValueError("O domínio deve ser uma string com até 255 caracteres.")
        if not value.strip():
            raise ValueError("O domínio não pode estar vazio.")
        return value.strip().lower()

    @validates('requests', 'blocks')
    def validate_non_negative(self, key, value):
        """Garante que os campos `requests` e `blocks` sejam valores não negativos."""
        if value < 0:
            raise ValueError(f"O campo '{key}' não pode ser negativo.")
        return value

    def to_dict(self):
        """Converte o objeto DNSData em um dicionário para facilitar a serialização."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "domain": self.domain,
            "requests": self.requests,
            "blocks": self.blocks,
            "threat_level": self.threat_level or "unknown",
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
            ),
        }
