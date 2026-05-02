import logging
from src.config.database import db
from src.models.category import Category
from src.models.task import Task
from src.config import settings

logger = logging.getLogger(__name__)


def list_categories():
    categories = Category.query.all()
    result = []
    for c in categories:
        data = c.to_dict()
        data['task_count'] = Task.query.filter_by(category_id=c.id).count()
        result.append(data)
    return result, 200


def create_category(data):
    if not data:
        return {'error': 'Dados inválidos'}, 400

    name = data.get('name', '').strip()
    if not name:
        return {'error': 'Nome é obrigatório'}, 400

    color = data.get('color', settings.DEFAULT_COLOR)
    if color and (len(color) != 7 or color[0] != '#'):
        return {'error': 'Cor inválida. Use formato #RRGGBB'}, 400

    category = Category(
        name=name,
        description=data.get('description', ''),
        color=color,
    )

    try:
        db.session.add(category)
        db.session.commit()
        logger.info('Category created id=%s', category.id)
        return category.to_dict(), 201
    except Exception as exc:
        db.session.rollback()
        logger.error('Error creating category: %s', exc)
        return {'error': 'Erro ao criar categoria'}, 500


def update_category(cat_id, data):
    category = db.session.get(Category, cat_id)
    if not category:
        return {'error': 'Categoria não encontrada'}, 404
    if not data:
        return {'error': 'Dados inválidos'}, 400

    if 'name' in data:
        category.name = data['name'].strip()
    if 'description' in data:
        category.description = data['description']
    if 'color' in data:
        color = data['color']
        if color and (len(color) != 7 or color[0] != '#'):
            return {'error': 'Cor inválida. Use formato #RRGGBB'}, 400
        category.color = color

    try:
        db.session.commit()
        logger.info('Category updated id=%s', cat_id)
        return category.to_dict(), 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error updating category %s: %s', cat_id, exc)
        return {'error': 'Erro ao atualizar'}, 500


def delete_category(cat_id):
    category = db.session.get(Category, cat_id)
    if not category:
        return {'error': 'Categoria não encontrada'}, 404
    try:
        Task.query.filter_by(category_id=cat_id).update({'category_id': None})
        db.session.delete(category)
        db.session.commit()
        logger.info('Category deleted id=%s', cat_id)
        return {'message': 'Categoria deletada'}, 200
    except Exception as exc:
        db.session.rollback()
        logger.error('Error deleting category %s: %s', cat_id, exc)
        return {'error': 'Erro ao deletar'}, 500
