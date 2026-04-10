import resend
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def send_contact_notification(name: str, email: str, subject: str, message: str, phone_number: str | None = None) -> None:
    api_key = os.getenv("RESEND_API_KEY")
    recipient = os.getenv("EMAIL_RECIPIENT")

    if not api_key or not recipient:
        logger.warning("Resend API key or recipient not set — email notification skipped.")
        return

    resend.api_key = api_key

    phone_line = f"Phone: {phone_number}\n" if phone_number else ""
    body = f"New contact form submission:\n\nName: {name}\nEmail: {email}\nSubject: {subject}\n{phone_line}Message:\n{message}"

    try:
        resend.Emails.send({
            "from": "Portfolio Contact Form <noreply@jacobrluttrull.com>",
            "to": recipient,
            "subject": f"[Portfolio] {subject} - from {name}",
            "text": body
        })
        logger.info(f"Contact notification sent for {name} ({email})")
    except Exception as e:
        logger.error(f"Failed to send contact notification: {e}")
