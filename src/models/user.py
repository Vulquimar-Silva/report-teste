from src.core.database import db
from flask_bcrypt import Bcrypt
from datetime import datetime
from src.core.logger import logger

bcrypt = Bcrypt()

class User(db.Model):
    """
    Modelo para representar usuários no banco de dados.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def password(self):
        """Impede que o hash da senha seja acessado diretamente."""
        raise AttributeError('A senha não pode ser lida diretamente.')

    @password.setter
    def password(self, password):
        """
        Gera o hash da senha e o armazena no banco de dados.
        """
        if len(password) < 8:
            logger.error("Falha ao definir senha: senha muito curta (menos de 8 caracteres).")
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")

        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        logger.info(f"Senha alterada com sucesso para o usuário {self.username}.")

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Converte o objeto User em um dicionário (exclui infos sensíveis)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
