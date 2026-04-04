import smtplib
import os
from email.mime.text import MIMEText


def send_contact_notification(name: str, email: str, message: str, phone_number: str | None = None) -> None:
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender or not password:
        return

    phone_line = f"Phone: {phone_number}\n" if phone_number else ""
    body = f"New contact form submission:\n\nName: {name}\nEmail: {email}\n{phone_line}Message:\n{message}"

    msg = MIMEText(body)
    msg["Subject"] = f"Portfolio Contact: {name}"
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())
