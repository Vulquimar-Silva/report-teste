from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from src.core.config import config
from src.models.user import User
from src.core.logger import logger

def token_required(f):
    """
    Decorador que:
     - Se REQUIRES_AUTH=False, chama o endpoint com current_user=None.
     - Caso contrário, valida o token JWT e chama o endpoint com current_user=User(...).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Se a autenticação estiver desativada via .env, chamamos a rota sem 'current_user'.
        if not getattr(config, "REQUIRES_AUTH", False):
            logger.debug("REQUIRES_AUTH=False, chamando endpoint sem current_user.")
            return f(None, *args, **kwargs)

        # Caso REQUIRES_AUTH=True, validamos o token JWT.
        token = None
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            else:
                logger.warning("Cabeçalho de autorização malformado.")
                return jsonify({'message': 'Authorization header malformado!'}), 401
        else:
            logger.warning("Cabeçalho de autorização ausente.")
            return jsonify({'message': 'Token não fornecido!'}), 401

        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            user_id = data.get('user_id')
            if not user_id:
                logger.error("Token JWT sem user_id.")
                return jsonify({'message': 'Token inválido!'}), 401

            current_user = User.query.filter_by(id=user_id).first()
            if not current_user:
                logger.error("Usuário não encontrado no banco para o token fornecido.")
                return jsonify({'message': 'Usuário não encontrado!'}), 401

        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado.")
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            logger.error("Token inválido ou malformado.")
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id):
    """
    Gera um token JWT com duração configurável (TOKEN_EXPIRATION_HOURS).
    """
    try:
        expiration_hours = int(getattr(config, "TOKEN_EXPIRATION_HOURS", 24))
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours)
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
        logger.info(f"Token gerado para usuário ID {user_id}, expira em {expiration_hours}h.")
        return token
    except Exception as e:
        logger.error(f"Erro ao gerar token para usuário ID {user_id}: {e}")
        raise
