import smtplib
import os
from email.mime.text import MIMEText


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

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
