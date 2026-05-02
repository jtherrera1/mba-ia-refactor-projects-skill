import logging
import smtplib
from datetime import datetime, timezone
from src.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self._history: list[dict] = []

    def send_email(self, to: str, subject: str, body: str) -> bool:
        if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
            logger.warning('Email not configured — skipping send to %s', to)
            return False
        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, to, f'Subject: {subject}\n\n{body}')
            server.quit()
            logger.info('Email sent to %s', to)
            return True
        except Exception as exc:
            logger.error('Failed to send email to %s: %s', to, exc)
            return False

    def notify_task_assigned(self, user, task) -> None:
        subject = f'Nova task atribuída: {task.title}'
        body = (
            f'Olá {user.name},\n\n'
            f"A task '{task.title}' foi atribuída a você.\n\n"
            f'Prioridade: {task.priority}\nStatus: {task.status}'
        )
        self.send_email(user.email, subject, body)
        self._history.append({
            'type': 'task_assigned',
            'user_id': user.id,
            'task_id': task.id,
            'timestamp': datetime.now(timezone.utc),
        })

    def notify_task_overdue(self, user, task) -> None:
        subject = f'Task atrasada: {task.title}'
        body = (
            f'Olá {user.name},\n\n'
            f"A task '{task.title}' está atrasada!\n\n"
            f'Data limite: {task.due_date}'
        )
        self.send_email(user.email, subject, body)

    def get_notifications(self, user_id: int) -> list[dict]:
        return [n for n in self._history if n['user_id'] == user_id]
