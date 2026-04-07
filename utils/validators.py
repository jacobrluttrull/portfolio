# this file I want to validate the data tha comes into the contact form on contact page. The requirements are as follows
# : Name — no special characters like !@#$%, not just whitespace, reasonable length (2-65 chars) (list of not allowed characters can be expanded as needed)
# Email — valid email format (has @, has a domain) (can use regex for this, but a simple check for "@" and "." in the right places can suffice for basic validation)
# Phone — if provided, only digits, dashes, parentheses, spaces, and +. Reasonable length. (7-20 chars and regex to ensure only allowed characters)
# Message — not empty, maybe a minimum length like 10 characters so you don't get "hi" (but this can be adjusted based on your needs)
import re
import html


def sanitize(text: str) -> str:
    """Escapes HTML characters to prevent XSS attacks.
    For example, <scripts>alert('hi')</scripts> becomes &lt;scripts&gt;alert('hi')&lt;/scripts&gt;
    This means the browser displays it as plain text instead of executing it."""
    return html.escape(text)


def validate_name(name: str) -> bool:
    name = name.strip()
    if len(name) < 2 or len(name) > 65:
        return False
    if any(char in name for char in "!@#$%^&*()_+=[]{}|\\:;\"'<>,.?/"):
        return False
    return True

def validate_email(email: str) -> bool:
    email = email.strip()
    if len(email) > 100:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(pattern, email):
        return True
    else:
        return False

def validate_subject(subject: str) -> bool:
    subject = subject.strip()
    pattern = r'^[\w\s.,!?\'\"()\-@#&:]+$'
    if not re.fullmatch(pattern, subject):
        return False
    if len(subject) < 2 or len(subject) > 200:
        return False
    return True

def validate_phone(phone: str) -> bool:
    phone = phone.strip()
    pattern = r"^\+?[\d\s\-()]{7,20}$"
    if re.fullmatch(pattern, phone):
        return True
    else:
        return False

def validate_message(message: str) -> bool:
    message = message.strip()
    if len(message) < 10 or len(message) > 2000:
        return False
    return True

def validate_url(url: str) -> bool:
    url = url.strip()
    if url.startswith("/static/"):
        return True
    pattern = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    if re.fullmatch(pattern, url):
        return True
    else:
        return False