import smtplib
from flask import current_app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..config import Config


def send(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = Config.SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}")
