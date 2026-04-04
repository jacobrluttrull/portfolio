from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Form
from starlette.responses import RedirectResponse

from models.contact import Contact
from typing import Annotated
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from models.project import Project
from utils.validators import validate_message, validate_email, validate_phone, validate_name, sanitize, validate_url, \
    validate_subject
from utils.email_notify import send_contact_notification

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
        db: Session = Depends(get_db)
):
    errors = []
    if not validate_name(name):
        errors.append("Invalid name. Please enter a valid name.")
    if not validate_email(email):
        errors.append("Invalid email. Please enter a valid email address.")
    if not validate_subject(subject):
        errors.append("Invalid subject. Please enter a subject that is at least 2 characters long. Allowed characters are letters, numbers, spaces, and basic punctuation .")
    if phone_number and not validate_phone(phone_number):
        errors.append("Invalid phone number. Please enter a valid phone number.")
    if not validate_message(message):
        errors.append("Invalid message. Please enter a message that is at least 10 characters long.")
    if errors:
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
        return templates.TemplateResponse("contact.html", {"request": request, "errors": ["Something went wrong. Please try again."], "name": name, "email": email, "subject": subject, "message": message, "phone_number": phone_number, "active_page": "contact"})


    send_contact_notification(name, email, subject, message, phone_number)
    #changing return to a RedirectResponse to avoid form resubmission on page refresh, but I want to pass a success message to the contact page. I can do this by adding a query parameter to the URL and checking for it in the GET request handler for the contact page.
    return RedirectResponse(url="/contact?success=true", status_code=302)



