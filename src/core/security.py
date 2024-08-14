from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from src.core.config import config
from src.models.user import User
from src.core.logger import logger

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                raise Exception("User not found")
        except Exception as e:
            logger.error(f"Token invalid: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, config.SECRET_KEY, algorithm="HS256")
    return token
