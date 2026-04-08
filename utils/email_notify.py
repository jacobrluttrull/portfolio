import smtplib
import os
import time
from utils.logger import get_logger
from email.mime.text import MIMEText

logger = get_logger(__name__)

def send_contact_notification(name: str, email: str, subject: str, message: str, phone_number: str | None = None) -> None:
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT")

    if not sender or not password or not recipient:
        return

    phone_line = f"Phone: {phone_number}\n" if phone_number else ""
    body = f"New contact form submission:\n\nName: {name}\nEmail: {email}\nSubject: {subject}\n{phone_line}Message:\n{message}"


    msg = MIMEText(body)
    msg["Subject"] = f"[Portfolio] {subject} New message from {name}"
    msg["From"] = f"Portfolio Contact Form <{sender}>"
    msg["To"] = recipient

    for i in range(3):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, recipient, msg.as_string())
            break
        except Exception as e:
            time.sleep(8)
            if i == 2:
                logger.error(f"Failed to send contact notification email after 3 attempts: {e}")




