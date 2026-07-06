import logging
import smtplib
from email.message import EmailMessage

from Core.Celery.CeleryApp import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def send_mail(
    recipient: str,
    body: str,
    mail_config: dict,
    subject: str,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_config["smtp_user"]
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(mail_config["smtp_server"], mail_config["smtp_port"]) as server:
        server.starttls()
        server.login(mail_config["smtp_user"], mail_config["smtp_password"])
        server.send_message(msg)

    logger.info("Mail sent to %s", recipient)
