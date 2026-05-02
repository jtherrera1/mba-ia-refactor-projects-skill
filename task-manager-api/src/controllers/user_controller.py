import logging
import re
from src.config.database import db
from src.models.user import User
from src.models.task import Task
from src.config import settings

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$')


def list_users():
    users = User.query.all()
    result = []
    for u in users:
        data = u.to_dict()
        data['task_count'] = len(u.tasks)
        result.append(data)
    return result, 200


def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': 'Usuário não encontrado'}, 404
    data = user.to_dict()
    data['tasks'] = [t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]
    return data, 200


def create_user(data):
    if not data:
        return {'error': 'Dados inválidos'}, 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', 'user')

    if not name:
        return {'error': 'Nome é obrigatório'}, 400
    if not email:
        return {'error': 'Email é obrigatório'}, 400
    if not password:
        return {'error': 'Senha é obrigatória'}, 400

    if not _EMAIL_RE.match(email):
        return {'error': 'Email inválido'}, 400
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        return {'error': 'Senha deve ter no mínimo 4 caracteres'}, 400
    if role not in settings.VALID_ROLES:
        return {'error': 'Role inválido'}, 400

    if User.query.filter_by(email=email).first():
        return {'error': 'Email já cadastrado'}, 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        logger.info('User created id=%s email=%s', user.id, user.email)
        return user.to_dict(), 201
    except Exception as exc:
        db.session.rollback()
        logger.error('Error creating user: %s', exc)
        return {'error': 'Erro ao criar usuário'}, 500


def update_user(user_id, data):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': 'Usuário não encontrado'}, 404
    if not data:
        return {'error': 'Dados inválidos'}, 400

    if 'name' in data:
        user.name = data['name'].strip()

    if 'email' in data:
        email = data['email'].strip()
        if not _EMAIL_RE.match(email):
            return {'error': 'Email inválido'}, 400
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return {'error': 'Email já cadastrado'}, 409
        user.email = email

    if 'password' in data:
        if len(data['password']) < settings.MIN_PASSWORD_LENGTH:
            return {'error': 'Senha muito curta'}, 400
        user.set_password(data['password'])

    if 'role' in data:
        if data['role'] not in settings.VALID_ROLES:
            return {'error': 'Role inválido'}, 400
        user.role = data['role']

    if 'active' in data:
        user.active = data['active']

    try:
        db.session.commit()
        logger.info('User updated id=%s', user_id)
        return user.to_dict(), 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error updating user %s: %s', user_id, exc)
        return {'error': 'Erro ao atualizar'}, 500


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': 'Usuário não encontrado'}, 404
    try:
        Task.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        logger.info('User deleted id=%s', user_id)
        return {'message': 'Usuário deletado com sucesso'}, 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error deleting user %s: %s', user_id, exc)
        return {'error': 'Erro ao deletar'}, 500


def get_user_tasks(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': 'Usuário não encontrado'}, 404
    result = []
    for t in Task.query.filter_by(user_id=user_id).all():
        data = t.to_dict()
        data['overdue'] = t.is_overdue()
        result.append(data)
    return result, 200


def login(data):
    if not data:
        return {'error': 'Dados inválidos'}, 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return {'error': 'Email e senha são obrigatórios'}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {'error': 'Credenciais inválidas'}, 401
    if not user.active:
        return {'error': 'Usuário inativo'}, 403

    return {
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token': f'fake-jwt-token-{user.id}',
    }, 200
