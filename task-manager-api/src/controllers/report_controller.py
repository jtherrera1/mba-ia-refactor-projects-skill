import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from src.config.database import db
from src.models.task import Task
from src.models.user import User
from src.models.category import Category

logger = logging.getLogger(__name__)


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def summary_report():
    total_tasks = db.session.query(func.count(Task.id)).scalar() or 0
    total_users = db.session.query(func.count(User.id)).scalar() or 0
    total_categories = db.session.query(func.count(Category.id)).scalar() or 0

    by_status = {
        s: db.session.query(func.count(Task.id)).filter(Task.status == s).scalar() or 0
        for s in ['pending', 'in_progress', 'done', 'cancelled']
    }
    by_priority = {
        label: db.session.query(func.count(Task.id)).filter(Task.priority == p).scalar() or 0
        for p, label in [(1, 'critical'), (2, 'high'), (3, 'medium'), (4, 'low'), (5, 'minimal')]
    }

    now = _utcnow()
    overdue_tasks = [
        t for t in Task.query.filter(
            Task.due_date < now,
            Task.status.notin_(['done', 'cancelled']),
        ).all()
    ]
    overdue_list = [
        {
            'id': t.id,
            'title': t.title,
            'due_date': str(t.due_date),
            'days_overdue': (now - t.due_date).days,
        }
        for t in overdue_tasks
    ]

    seven_days_ago = now - timedelta(days=7)
    recent_tasks = db.session.query(func.count(Task.id)).filter(Task.created_at >= seven_days_ago).scalar() or 0
    recent_done = db.session.query(func.count(Task.id)).filter(
        Task.status == 'done', Task.updated_at >= seven_days_ago
    ).scalar() or 0

    users = User.query.all()
    user_stats = []
    for u in users:
        user_tasks = Task.query.filter_by(user_id=u.id).all()
        total = len(user_tasks)
        completed = sum(1 for t in user_tasks if t.status == 'done')
        user_stats.append({
            'user_id': u.id,
            'user_name': u.name,
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0,
        })

    return {
        'generated_at': str(now),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': total_users,
            'total_categories': total_categories,
        },
        'tasks_by_status': by_status,
        'tasks_by_priority': by_priority,
        'overdue': {'count': len(overdue_list), 'tasks': overdue_list},
        'recent_activity': {
            'tasks_created_last_7_days': recent_tasks,
            'tasks_completed_last_7_days': recent_done,
        },
        'user_productivity': user_stats,
    }, 200


def user_report(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': 'Usuário não encontrado'}, 404

    tasks = Task.query.filter_by(user_id=user_id).all()
    total = len(tasks)
    counts = {'done': 0, 'pending': 0, 'in_progress': 0, 'cancelled': 0}
    overdue = 0
    high_priority = 0

    for t in tasks:
        if t.status in counts:
            counts[t.status] += 1
        if t.priority <= 2:
            high_priority += 1
        if t.is_overdue():
            overdue += 1

    return {
        'user': {'id': user.id, 'name': user.name, 'email': user.email},
        'statistics': {
            'total_tasks': total,
            **counts,
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': round((counts['done'] / total) * 100, 2) if total > 0 else 0,
        },
    }, 200
