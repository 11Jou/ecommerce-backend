import logging
import smtplib
from email.message import EmailMessage

from Core.Celery.CeleryApp import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def send_activation_mail(
    recipient: str,
    body: str,
    smtp_user: str,
    smtp_password: str,
    smtp_server: str,
    smtp_port: int,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Activate your account"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    logger.info("Activation mail sent to %s", recipient)
