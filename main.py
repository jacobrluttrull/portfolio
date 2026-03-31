from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import engine, Base
from models.contact import Contact
from models.project import Project
from routers import pages, admin



Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    raise exc

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(admin.router)
app.include_router(pages.router)
