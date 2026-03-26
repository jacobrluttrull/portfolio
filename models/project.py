from database import Base
from sqlalchemy import Column, Integer, String, Text

# Defining the Project Model which will include the Title, Description, Tech Stack, link to project (GitHub), image of project (optional),  and duration of project

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(Text, nullable=False)
    github_link = Column(String(200), nullable=False)
    image_url = Column(String(200))
    duration = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False)  # New field for display order
