import utils.auth as auth

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models.project import Project
from fastapi.responses import RedirectResponse
from utils.validators import sanitize, validate_url
from utils.logger import get_logger


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = get_logger(__name__)
templates = Jinja2Templates(directory="templates")

async def require_admin(request: Request):
    token = request.cookies.get("admin_token")
    if not token or not auth.verify_jwt_token(token):
        raise HTTPException(status_code=302, headers={"Location": "/admin/login"})

@router.get("/admin/login")
async def login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/admin/login")
@limiter.limit("5/minute")
async def login_verify(request: Request, password: str = Form()):
    if auth.verify_password(password):
        token = auth.create_jwt_token()
        logger.info("Admin login successful")
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie("admin_token", value=token, httponly=True, secure=True, samesite="Strict")
        return response
    else:
        logger.warning(f"Failed admin login attempt from {request.client.host}")
        return templates.TemplateResponse("admin/login.html", {"request": request, "error": "Invalid password."})

@router.get("/admin/logout")
async def logout():
    logger.info("Admin logged out")
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("admin_token")
    return response

@router.get("/admin")
async def admin_dashboard(request: Request, db: Session = Depends(get_db), admin: bool = Depends(require_admin)):
    projects = db.query(Project).order_by(Project.display_order).all()
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "projects": projects})

@router.get("/admin/add")
async def add_project_form(request: Request, admin: bool = Depends(require_admin)):
    return templates.TemplateResponse("admin/add.html", {"request": request})

@router.post("/admin/add")
async def add_project(
    request: Request,
    title: str = Form(),
    description: str = Form(),
    tech_stack: str = Form(),
    github_link: str = Form(),
    image_url: str | None = Form(default=None),
    duration: str = Form(),
    display_order: int = Form(),
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    if not validate_url(github_link):
        return templates.TemplateResponse("admin/add.html", {"request": request, "error": "Invalid GitHub link. Please enter a valid URL."})
    if image_url and not validate_url(image_url):
        return templates.TemplateResponse("admin/add.html", {"request": request, "error": "Invalid image URL. Please enter a valid URL."})
    new_project = Project(
        title=sanitize(title),
        description=sanitize(description),
        tech_stack=sanitize(tech_stack),
        github_link=sanitize(github_link),
        image_url=image_url,
        duration=sanitize(duration),
        display_order=display_order
    )
    try:
        db.add(new_project)
        db.commit()
        logger.info(f"Project added: {title}")
    except SQLAlchemyError:
        db.rollback()
        logger.exception(f"DB error adding project: {title}")
        return templates.TemplateResponse("admin/add.html", {"request": request, "error": "Failed to save project. Please try again."})
    return RedirectResponse(url="/admin", status_code=302)

@router.post("/admin/delete/{project_id}")
async def delete_project(request: Request, project_id: int, db: Session = Depends(get_db), admin: bool = Depends(require_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        try:
            db.delete(project)
            db.commit()
            logger.info(f"Project deleted: {project.title} (id={project_id})")
        except SQLAlchemyError:
            db.rollback()
            logger.exception(f"DB error deleting project id={project_id}")
    return RedirectResponse(url="/admin", status_code=302)

@router.get("/admin/edit/{project_id}")
async def edit_project(request: Request, project_id: int, db: Session = Depends(get_db), admin: bool = Depends(require_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("admin/edit.html", {"request": request, "project": project})

@router.post("/admin/edit/{project_id}")
async def update_project(
    request: Request,
    project_id: int,
    title: str = Form(),
    description: str = Form(),
    tech_stack: str = Form(),
    github_link: str = Form(),
    image_url: str | None = Form(default=None),
    duration: str = Form(),
    display_order: int = Form(),
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        if not validate_url(github_link):
            return templates.TemplateResponse("admin/edit.html", {"request": request, "project": project, "error": "Invalid GitHub link. Please enter a valid URL."})
        if image_url and not validate_url(image_url):
            return templates.TemplateResponse("admin/edit.html", {"request": request, "project": project, "error": "Invalid image URL. Please enter a valid URL."})
        project.title = sanitize(title)
        project.description = sanitize(description)
        project.tech_stack = sanitize(tech_stack)
        project.github_link = sanitize(github_link)
        project.image_url = image_url
        project.duration = sanitize(duration)
        project.display_order = display_order
        try:
            db.commit()
            logger.info(f"Project updated: {title} (id={project_id})")
        except SQLAlchemyError:
            db.rollback()
            logger.exception(f"DB error updating project id={project_id}")
            return templates.TemplateResponse("admin/edit.html", {"request": request, "project": project, "error": "Failed to update project. Please try again."})
    return RedirectResponse(url="/admin", status_code=302)
