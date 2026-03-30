# This is a script to seed projects into the database. It can be run with `python scripts/seed_projects.py` and will create some sample projects for testing purposes.

import sys
sys.path.append(".")

from database import SessionLocal, engine, Base
from models.project import Project

# I'm going to seed 4 of my main projects into this database. Each project will have a title, description, tech stack, GitHub link, image URL (optional), duration, and display order.

def seed_projects():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    projects = [
        Project(
            title= "Oklahoma Sooners Dashboard",
            description= "A Django-powered college football dashboard that pulls live data from the CFBD API."
                         " Displays season records, AP rankings, player stat leaders, an annotated schedule, and game box scores. Features idempotent data syncing, caching for performance, "
                         "and a custom management command for refreshing stats. ",
            tech_stack= "Python, Django, SQLite, CFBD API, Bootstrap",
            github_link= "https://github.com/jacobrluttrull/oklahoma_sooners_dashboard",
            image_url = "/static/images/ousoonerproject.jpg",
            duration = "October 2025 - November 2025",
            display_order = 1

        ),
        Project(
            title= "Type 2 Diabetes Prediction Website (Capstone Project)",
            description= "A machine learning capstone project that predicts Type 2 Diabetes risk using patient health metrics. Built with Streamlit, featuring an interactive dashboard with SHAP explainability, ROC/PR visualizations, adjustable classification thresholds, and CSV export. Includes a calibrated scikit-learn pipeline with probability scoring.",
            tech_stack= "Python, Streamlit, scikit-learn, matplotlip, pandas, jupyter notebook, SHAP",
            github_link= "https://github.com/jacobrluttrull/prod-diabetic-capstone",
            image_url = "/static/images/diabetic.png",
            duration = "August 2025, September 2025",
            display_order = 2
        ),
        Project(
            title= "Static Site Generator",
            description= "This is a Python project from scratch that converts Markdown content into fully static HTML/CSS files.",
            tech_stack= "Python, GitHub Pages, Markdown",
            github_link= "https://github.com/jacobrluttrull/static_site_generator",
            image_url = "/static/images/staticsite.png",
            duration = "February 2026",
            display_order = 3
        ),
        Project(
            title = "AI Chatbot using OpenAI API",
            description = "AI_Bot is a command-line AI coding assistant built in Python that can interact with a local project through a controlled set of tools. It supports both one-shot prompts and an interactive REPL mode, allowing the assistant to inspect files, write changes, execute Python scripts, and run automated tests.",
            tech_stack = "Python, OpenAI API, pytest, Linux, uv",
            github_link = "https://github.com/jacobrluttrull/AI_Bot",
            image_url = "/static/images/aibot.png",
            duration = "January 2026 - February 2026",
            display_order = 4



        )

    ]
    if db.query(Project).count() > 0:
        print("Projects already seeded. Skipping seeding to avoid duplicates.")
        db.close()
        return
    for project in projects:
        db.add(project)
    db.commit()
    db.close()
seed_projects()