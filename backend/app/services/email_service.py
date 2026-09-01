import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from backend.app.core.config import settings


class EmailService:
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, username: Optional[str] = None, password: Optional[str] = None, from_email: Optional[str] = None, use_tls: Optional[bool] = None):
        self.host = host or settings.smtp_host
        self.port = port or settings.smtp_port
        self.username = username or settings.smtp_user
        self.password = password or settings.smtp_password
        self.from_email = from_email or settings.smtp_from_email
        self.use_tls = use_tls if use_tls is not None else settings.smtp_tls

    def send_email(self, recipient: str, subject: str, message_content: str, html: bool = False) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = recipient
        msg['Subject'] = subject

        subtype = 'html' if html else 'plain'

        msg.attach(MIMEText(message_content, subtype, 'utf-8'))

        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()

            if self.username and self.password:
                server.login(self.username, self.password)

            server.send_message(msg)

email_service = EmailService()


