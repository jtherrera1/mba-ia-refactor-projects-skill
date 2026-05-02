import logging
from datetime import datetime
from sqlalchemy.orm import joinedload
from src.config.database import db
from src.models.task import Task
from src.models.user import User
from src.models.category import Category
from src.config import settings

logger = logging.getLogger(__name__)


def list_tasks():
    tasks = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).all()
    result = []
    for t in tasks:
        data = t.to_dict()
        data['overdue'] = t.is_overdue()
        data['user_name'] = t.user.name if t.user else None
        data['category_name'] = t.category.name if t.category else None
        result.append(data)
    return result, 200


def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {'error': 'Task não encontrada'}, 404
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    return data, 200


def create_task(data):
    if not data:
        return {'error': 'Dados inválidos'}, 400

    title = data.get('title', '').strip()
    if not title:
        return {'error': 'Título é obrigatório'}, 400
    if len(title) < settings.MIN_TITLE_LENGTH:
        return {'error': 'Título muito curto'}, 400
    if len(title) > settings.MAX_TITLE_LENGTH:
        return {'error': 'Título muito longo'}, 400

    status = data.get('status', 'pending')
    if status not in settings.VALID_STATUSES:
        return {'error': 'Status inválido'}, 400

    priority = data.get('priority', settings.DEFAULT_PRIORITY)
    if not (settings.MIN_PRIORITY <= priority <= settings.MAX_PRIORITY):
        return {'error': 'Prioridade deve ser entre 1 e 5'}, 400

    user_id = data.get('user_id')
    if user_id and not db.session.get(User, user_id):
        return {'error': 'Usuário não encontrado'}, 404

    category_id = data.get('category_id')
    if category_id and not db.session.get(Category, category_id):
        return {'error': 'Categoria não encontrada'}, 404

    task = Task(
        title=title,
        description=data.get('description', ''),
        status=status,
        priority=priority,
        user_id=user_id,
        category_id=category_id,
    )

    due_date = data.get('due_date')
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return {'error': 'Formato de data inválido. Use YYYY-MM-DD'}, 400

    tags = data.get('tags')
    if tags:
        task.tags = ','.join(tags) if isinstance(tags, list) else tags

    try:
        db.session.add(task)
        db.session.commit()
        logger.info('Task created id=%s title=%s', task.id, task.title)
        return task.to_dict(), 201
    except Exception as exc:
        db.session.rollback()
        logger.error('Error creating task: %s', exc)
        return {'error': 'Erro ao criar task'}, 500


def update_task(task_id, data):
    task = db.session.get(Task, task_id)
    if not task:
        return {'error': 'Task não encontrada'}, 404
    if not data:
        return {'error': 'Dados inválidos'}, 400

    if 'title' in data:
        title = data['title'].strip()
        if len(title) < settings.MIN_TITLE_LENGTH:
            return {'error': 'Título muito curto'}, 400
        if len(title) > settings.MAX_TITLE_LENGTH:
            return {'error': 'Título muito longo'}, 400
        task.title = title

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        if data['status'] not in settings.VALID_STATUSES:
            return {'error': 'Status inválido'}, 400
        task.status = data['status']

    if 'priority' in data:
        if not (settings.MIN_PRIORITY <= data['priority'] <= settings.MAX_PRIORITY):
            return {'error': 'Prioridade deve ser entre 1 e 5'}, 400
        task.priority = data['priority']

    if 'user_id' in data:
        if data['user_id'] and not db.session.get(User, data['user_id']):
            return {'error': 'Usuário não encontrado'}, 404
        task.user_id = data['user_id']

    if 'category_id' in data:
        if data['category_id'] and not db.session.get(Category, data['category_id']):
            return {'error': 'Categoria não encontrada'}, 404
        task.category_id = data['category_id']

    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return {'error': 'Formato de data inválido'}, 400
        else:
            task.due_date = None

    if 'tags' in data:
        tags = data['tags']
        task.tags = ','.join(tags) if isinstance(tags, list) else tags

    try:
        db.session.commit()
        logger.info('Task updated id=%s', task_id)
        return task.to_dict(), 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error updating task %s: %s', task_id, exc)
        return {'error': 'Erro ao atualizar'}, 500


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {'error': 'Task não encontrada'}, 404
    try:
        db.session.delete(task)
        db.session.commit()
        logger.info('Task deleted id=%s', task_id)
        return {'message': 'Task deletada com sucesso'}, 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error deleting task %s: %s', task_id, exc)
        return {'error': 'Erro ao deletar'}, 500


def search_tasks(query='', status='', priority='', user_id=''):
    tasks_q = Task.query
    if query:
        tasks_q = tasks_q.filter(
            db.or_(
                Task.title.like(f'%{query}%'),
                Task.description.like(f'%{query}%'),
            )
        )
    if status:
        tasks_q = tasks_q.filter(Task.status == status)
    if priority:
        tasks_q = tasks_q.filter(Task.priority == int(priority))
    if user_id:
        tasks_q = tasks_q.filter(Task.user_id == int(user_id))
    return [t.to_dict() for t in tasks_q.all()], 200


def get_task_stats():
    from sqlalchemy import func
    total = db.session.query(func.count(Task.id)).scalar() or 0
    by_status = {
        s: db.session.query(func.count(Task.id)).filter(Task.status == s).scalar() or 0
        for s in settings.VALID_STATUSES
    }
    overdue_count = sum(1 for t in Task.query.all() if t.is_overdue())
    done = by_status.get('done', 0)
    return {
        'total': total,
        **by_status,
        'overdue': overdue_count,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
    }, 200
