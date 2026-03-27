from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from models.contact import Contact
from models.project import Project
from routers import pages

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages.router)
