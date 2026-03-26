# Project Context for Claude Code

## About Me
I am a new CS grad actively job searching while building my portfolio. I completed a CS degree at WGU and hold several certifications. I am working through the Boot.dev backend development curriculum as my primary learning path.

**Skills:** Python, Django, Flask, Streamlit, C memory management, DSA, Git  
**Background:** Built projects including a static site generator, AI coding agent with OpenAI integration, Git clone in Python, and DSA/GC implementations in C  
**Next up:** Go via Boot.dev after this project

## How I Work
- Guidance-based approach — nudges over full solutions
- I attempt code first, then ask for help
- Keep code snippets to 25-50 lines max
- Point out bugs without fixing everything — let me correct them
- Help me stay in the current phase: Planning → Coding → Debugging → Polishing → Publishing
- Push back if I'm going down the wrong path
- Ask guiding questions before giving answers when I'm stuck

## Project: Portfolio Site
A personal portfolio site to showcase my work to employers.

**Stack:**
- Python / FastAPI
- Jinja2 templates
- Bootstrap (frontend)
- SQLAlchemy + SQLite (database)
- Deployed live (platform TBD)

**Pages:**
- `/` — home / about me
- `/projects` — pulled from SQLite database
- `/resume` — static page with downloadable PDF placeholder
- `/contact` — form that stores submissions in SQLite

**DB Models:**
- `Project` — title, description, tech stack, GitHub link
- `ContactMessage` — name, email, message, timestamp

**Current phase:** Coding  
**Current status:** `main.py` and `database.py` complete, models next

## File Structure
```
portfolio/
├── routers/
│   ├── pages.py
│   └── contact.py
├── models/
│   ├── project.py
│   └── contact.py
├── templates/
│   ├── base.html
│   └── index.html
├── static/
├── main.py
├── database.py
├── .env
└── requirements.txt
```