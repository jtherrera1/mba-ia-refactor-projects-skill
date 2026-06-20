import jwt
from functools import wraps
from flask import request, jsonify, g
from src.config.settings import JWT_SECRET_KEY


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1]

        if not token:
            return jsonify({'error': 'Token de autenticação não fornecido'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            g.current_user_id = payload['user_id']
            g.current_user_role = payload.get('role', 'user')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if g.current_user_role != 'admin':
            return jsonify({'error': 'Acesso restrito a administradores'}), 403
        return f(*args, **kwargs)
    return decorated
