import os

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Form
from starlette.responses import RedirectResponse
import httpx
from utils.logger import get_logger
from models.contact import Contact
from typing import Annotated
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from models.project import Project
from utils.validators import validate_message, validate_email, validate_phone, validate_name, sanitize, validate_url, \
    validate_subject
from utils.email_notify import send_contact_notification

router = APIRouter()
logger = get_logger(__name__)
templates = Jinja2Templates(directory="templates")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_page": "home"})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "active_page": "about"})


@router.get("/projects")
async def projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.display_order).all()
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects, "active_page": "projects"})


@router.get("/contact")
async def contact(request: Request, success: str | None = None):
    return templates.TemplateResponse("contact.html", {"request": request, "active_page": "contact", "success": success})


@router.post("/contact")
async def contact_submit(
        request: Request,
        name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        subject: Annotated[str, Form()],
        message: Annotated[str, Form()],
        phone_number: Annotated[str | None, Form()] = None,
        turnstile_token: Annotated[str, Form(alias="cf-turnstile-response")] = "",
        db: Session = Depends(get_db)
):
    errors = []
    if not validate_name(name):
        errors.append("Name must be between 2-65 characters and contain no special characters.")
    if not validate_email(email):
        errors.append("Please enter a valid email address (e.g. name@example.com).")
    if not validate_subject(subject):
        errors.append("Subject must be between 2-200 characters. Only letters, numbers, and basic punctuation allowed.")
    if phone_number and not validate_phone(phone_number):
        errors.append("Phone must be 7-20 characters and only contain digits, spaces, dashes, parentheses, or +.")
    if not validate_message(message):
        errors.append("Invalid message. Please enter a message that is at least 10 characters long.")
    if errors:
        return templates.TemplateResponse("contact.html", {"request": request, "errors": errors, "name": name, "email": email, "subject": subject, "message": message, "phone_number": phone_number, "active_page": "contact"})

    async with httpx.AsyncClient() as client:
        r = await client.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", data={
            "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
            "response": turnstile_token
        })
    #print(r.json()) #testing to see the response from cloudflare turnstile, I want to make sure I'm sending the request correctly and handling the response correctly. The expected response should have a "success" field that is true if the verification passed, and false if it failed. It may also have an "error-codes" field with more information about why it failed if it did.
    if not r.json().get("success"):
        errors.append("Verification failed. Please try again.")
        logger.warning(f"Turnstile Verification failed for {email}.")
        return templates.TemplateResponse("contact.html", {"request": request, "errors": errors, "name": name, "email": email, "subject": subject, "message": message, "phone_number": phone_number, "active_page": "contact"})


    contact_entry = Contact(
        name=sanitize(name.strip()),
        email=sanitize(email.strip()),
        subject=sanitize(subject.strip()),
        message=sanitize(message.strip()),
        phone_number=sanitize(phone_number.strip()) if phone_number else None

    )
    try:
        db.add(contact_entry)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception(f"DB error while saving contact form submission from {email}.")
        return templates.TemplateResponse("contact.html", {"request": request, "errors": ["Something went wrong. Please try again."], "name": name, "email": email, "subject": subject, "message": message, "phone_number": phone_number, "active_page": "contact"})


    send_contact_notification(name, email, subject, message, phone_number)
    #changing return to a RedirectResponse to avoid form resubmission on page refresh, but I want to pass a success message to the contact page. I can do this by adding a query parameter to the URL and checking for it in the GET request handler for the contact page.
    logger.info(f"New contact form submission: Name={name}, Email={email}, Subject={subject}, Phone={phone_number}")
    return RedirectResponse(url="/contact?success=true", status_code=302)



