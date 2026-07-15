# Source of truth for project content. Running this (locally or against Railway's
# DATABASE_URL) syncs the database to match this list exactly: existing projects
# (matched by title) get their fields updated, new ones get inserted, and any
# project in the database that's no longer listed here gets removed.

import sys
sys.path.append(".")

from database import SessionLocal, engine, Base
from models.project import Project

def seed_projects():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        projects = [
            Project(
                title= "Oklahoma Sooners Dashboard",
                description= "A Django-powered college football dashboard that pulls live data from the CFBD API."
                             " Displays season records, AP rankings, player stat leaders, an annotated schedule, and game box scores. Features idempotent data syncing, caching for performance, "
                             "and a custom management command for refreshing stats. ",
                tech_stack= "Python, Django, SQLite, CFBD API, Bootstrap",
                github_link= "https://github.com/jacobrluttrull/oklahoma_sooners_dashboard",
                image_url = "/static/images/ousoonerproject.webp",
                duration = "October 2025 - November 2025",
                display_order = 1

            ),
            Project(
                title= "Type 2 Diabetes Prediction Website (Capstone Project)",
                description= "A machine learning capstone project that predicts Type 2 Diabetes risk using patient health metrics. Built with Streamlit, featuring an interactive dashboard with SHAP explainability, ROC/PR visualizations, adjustable classification thresholds, and CSV export. Includes a calibrated scikit-learn pipeline with probability scoring.",
                tech_stack= "Python, Streamlit, scikit-learn, matplotlib, pandas, Jupyter Notebook, SHAP",
                github_link= "https://github.com/jacobrluttrull/prod-diabetic-capstone",
                image_url = "/static/images/diabetic.webp",
                duration = "August 2025, September 2025",
                display_order = 2
            ),
            Project(
                title = "Gator (RSS Feed Aggregator)",
                description = "A CLI RSS feed aggregator written in Go, backed by PostgreSQL. Users register, follow and unfollow RSS feeds, and Gator continuously fetches new posts from the least-recently-updated feed on a timer, storing them in the database for browsing from the terminal.",
                tech_stack = "Go, PostgreSQL, sqlc, goose",
                github_link = "https://github.com/jacobrluttrull/gator",
                image_url = "/static/images/rssagg.webp",
                duration = "July 2026",
                display_order = 3
            ),
            Project(
                title= "Static Site Generator",
                description= "This is a Python project from scratch that converts Markdown content into fully static HTML/CSS files.",
                tech_stack= "Python, GitHub Pages, Markdown",
                github_link= "https://github.com/jacobrluttrull/static_site_generator",
                image_url = "/static/images/staticsite.webp",
                duration = "February 2026",
                display_order = 4
            ),
            Project(
                title = "AI Chatbot using OpenAI API",
                description = "AI_Bot is a command-line AI coding assistant built in Python that can interact with a local project through a controlled set of tools. It supports both one-shot prompts and an interactive REPL mode, allowing the assistant to inspect files, write changes, execute Python scripts, and run automated tests.",
                tech_stack = "Python, OpenAI API, pytest, Linux, uv",
                github_link = "https://github.com/jacobrluttrull/AI_Bot",
                image_url = "/static/images/aibot.webp",
                duration = "January 2026 - February 2026",
                display_order = 5
            ),
            Project(
                title = "Pokedex CLI",
                description = "A command-line Pokedex built in Go that queries the PokeAPI to explore Pokémon locations, catch Pokémon, and inspect their stats. Features a REPL-style interface with in-memory caching. Built as part of the Boot.dev Go curriculum.",
                tech_stack = "Go, PokeAPI, HTTP",
                github_link = "https://github.com/jacobrluttrull/pokedex",
                image_url = "/static/images/pokedexcli.webp",
                duration = "June 2026",
                display_order = 6
            ),
            Project(
                title = "Git Clone in Python",
                description = "A hands-on implementation of Git internals in Python, following the Write Yourself a Git tutorial. Covers core Git concepts like objects, refs, and commits from scratch.",
                tech_stack = "Python",
                github_link = "https://github.com/jacobrluttrull/python_git",
                image_url = "/static/images/pythongit.webp",
                duration = "November 2025 - January 2026",
                display_order = 7
            ),
            Project(
                title = "Package Route Optimizer (WGU Project)",
                description = "A delivery routing simulation for WGUPS using a custom chaining hash table and greedy nearest-neighbor algorithm to minimize mileage across three trucks. Handles real-world constraints like deadlines, delayed packages, and grouped deliveries.",
                tech_stack = "Python, Data Structures & Algorithms",
                github_link = "https://github.com/jacobrluttrull/package-routing-optimizer",
                image_url = "/static/images/packageoptimizer.webp",
                duration = "September 2025",
                display_order = 8
            ),
            Project(
                title = "Movie Database Project",
                description = "WGU coursework project demonstrating PostgreSQL database design and reporting. Includes custom user-defined functions, triggers, stored procedures, and automated report generation from the DVD dataset.",
                tech_stack = "PostgreSQL, SQL",
                github_link = "https://github.com/jacobrluttrull/D326-adv-data-mgmnt",
                image_url = "/static/images/database326.webp",
                duration = "June 2024",
                display_order = 9
            ),
            Project(
                title = "Asteroids Game",
                description = "A recreation of the classic Asteroids arcade game built with Python and Pygame as part of the Boot.dev curriculum. Features OOP design with player movement, shooting mechanics, collision detection, and destructible asteroids.",
                tech_stack = "Python, Pygame",
                github_link = "https://github.com/jacobrluttrull/asteroidsgame",
                image_url = "/static/images/asteroids.webp",
                duration = "December 2025",
                display_order = 10
            ),
        ]

        seed_titles = {p.title for p in projects}
        inserted, updated = 0, 0

        for p in projects:
            matches = db.query(Project).filter_by(title=p.title).order_by(Project.id).all()
            existing, dupes = (matches[0], matches[1:]) if matches else (None, [])
            for dupe in dupes:
                db.delete(dupe)
            if existing:
                existing.description = p.description
                existing.tech_stack = p.tech_stack
                existing.github_link = p.github_link
                existing.image_url = p.image_url
                existing.duration = p.duration
                existing.display_order = p.display_order
                updated += 1
            else:
                db.add(p)
                inserted += 1

        removed = db.query(Project).filter(Project.title.notin_(seed_titles)).delete(synchronize_session=False)

        db.commit()
        print(f"Synced projects: {inserted} inserted, {updated} updated, {removed} removed.")
    except Exception as e:
        db.rollback()
        print(f"Error syncing projects: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_projects()