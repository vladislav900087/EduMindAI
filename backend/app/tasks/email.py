from backend.app.core.celery_app import celery_app
from backend.app.services.email_service import email_service

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, recipient: str, subject: str, message_content: str):
    try:
        email_service.send_email(recipient=recipient, subject=subject, message_content=message_content)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


