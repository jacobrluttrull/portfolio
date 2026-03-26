from fastapi import FastAPI

from database import engine, Base
from models.contact import Contact
from models.project import Project

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



