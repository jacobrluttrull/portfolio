# Portfolio
Jacob Luttrull's personal portfolio website showcasing projects, skills, and contact info.

## Tech Stack
- Python / FastAPI
- SQLAlchemy + SQLite
- Jinja2 templates
- Bootstrap 5.3
- JWT authentication (admin)

## Features
- Home / hero section with social links
- About page with skills, education, resume download
- Projects section (database-driven, admin-managed)
- Contact form (validated, stored in SQLite)
- Admin panel (JWT-protected CRUD for projects)
- Custom 404 page
- Responsive design (mobile + desktop)

## Project Structure
```
portfolio/
├── main.py                  # App init, routing, exception handlers
├── database.py              # SQLAlchemy engine, session, Base
├── requirements.txt
│
├── models/
│   ├── contact.py           # Contact form submissions
│   └── project.py           # Portfolio projects
│
├── routers/
│   ├── pages.py             # Public routes (/, /about, /projects, /contact)
│   └── admin.py             # Admin routes (/admin/*) — requires ENABLE_ADMIN=true
│
├── utils/
│   ├── auth.py              # JWT creation/verification, bcrypt password check
│   └── validators.py        # Input validation + XSS sanitization
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── projects.html
│   ├── contact.html
│   ├── 404.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── add.html
│       └── edit.html
│
├── static/
│   ├── css/style.css
│   ├── images/
│   ├── favicon/
│   └── resume/
│
└── scripts/
    └── seed_projects.py     # Seed DB with sample projects
```

## Environment Variables
Copy `.env.example` (when created) and fill in:
- `ADMIN_PASSWORD_HASH` — bcrypt hash of your admin password
- `JWT_SECRET` — strong random secret for token signing
- `ENABLE_ADMIN` — set to `true` to enable the admin panel

## Running Locally
1. Clone the repo
2. Create and activate a virtual environment
3. `pip install -r requirements.txt`
4. Set up your `.env` file
5. `uvicorn main:app --reload`
6. Visit `http://localhost:8000`

## Status
In development.
