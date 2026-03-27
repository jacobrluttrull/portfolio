from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Form
from models.contact import Contact
from typing import Annotated
from database import SessionLocal
from models.project import Project
from utils.validators import validate_message, validate_email, validate_phone, validate_name, sanitize

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/projects")
async def projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.display_order).all()
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})


@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/contact")
async def contact_submit(
        request: Request,
        name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        message: Annotated[str, Form()],
        phone_number: Annotated[str | None, Form()] = None,
        db: Session = Depends(get_db)
):
    errors = []
    if not validate_name(name):
        errors.append("Invalid name. Please enter a valid name.")
    if not validate_email(email):
        errors.append("Invalid email. Please enter a valid email address.")
    if phone_number and not validate_phone(phone_number):
        errors.append("Invalid phone number. Please enter a valid phone number.")
    if not validate_message(message):
        errors.append("Invalid message. Please enter a message that is at least 10 characters long.")
    if errors:
        return templates.TemplateResponse("contact.html", {"request": request, "errors": errors, "name": name, "email": email, "message": message, "phone_number": phone_number})

    contact_entry = Contact(
        name=sanitize(name.strip()),
        email=sanitize(email.strip()),
        message=sanitize(message.strip()),
        phone_number=sanitize(phone_number.strip()) if phone_number else None

    )
    db.add(contact_entry)
    db.commit()
    return templates.TemplateResponse("contact.html", {"request": request, "success": True})



