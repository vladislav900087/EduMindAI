from celery import Celery

from backend.app.core.config import settings

celery_app = Celery("backend", broker=settings.celery_broker_url, backend=settings.celery_broker_url, include=["backend.app.tasks.email", 'backend.app.tasks.notifications', 'backend.app.tasks.deadlines'], task_track_started=True)


celery_app.conf.update(
    task_track_started=True,
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        "send-assignment-deadline-reminders-every-15-minutes": {
            'task': 'backend.app.tasks.deadlines.send_assignment_deadline_reminders',
            'schedule': 15.0
        },
    },
)