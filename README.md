# Portfolio
Jacob Luttrull's personal portfolio website showcasing projects, skills, and contact info.

## Link to Site
[jacobrluttrull.com](https://jacobrluttrull.com)


## Tech Stack
- Python / FastAPI
- SQLAlchemy + PostgreSQL
- Alembic (database migrations)
- Jinja2 templates
- Bootstrap 5.3
- JWT authentication (admin)
- Cloudflare Turnstile (CAPTCHA)
- Resend (email notifications)
- Claude Code (AI-assisted development)

## Features
- Home page: hero (name, tagline, resume download, social links — GitHub, LinkedIn, Instagram, Discord, Email) followed by About/Skills/Education on the same page (`/about` 301-redirects to `/`)
- Light/dark theme toggle — auto-detects OS preference, manual override persisted in `localStorage`
- Projects section (database-driven, admin-managed, git is the source of truth via an upsert-and-prune seed sync) — split into a Featured tier (image, tech chips, optional highlight) and a compact list for the rest
- Contact form with validation, XSS sanitization, CSRF protection, Turnstile CAPTCHA, and email notifications
- Rate limiting on contact form and admin login
- Admin panel (JWT-protected CRUD for projects)
- Security headers middleware (X-Frame-Options, HSTS, CSP, etc.)
- Custom 404 page
- Rotating file logging
- Responsive design (mobile + desktop)

## Project Structure
```
portfolio/
├── main.py                  # App init, routing, middleware, exception handlers
├── database.py              # SQLAlchemy engine, session, Base
├── requirements.txt
├── Procfile                 # Railway deployment start command
│
├── alembic/                 # Database migrations
│   └── versions/
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
│   ├── validators.py        # Input validation + XSS sanitization
│   ├── email_notify.py      # Email notifications on contact form submission
│   └── logger.py            # App-wide logging setup
│
├── templates/
│   ├── base.html             # Shell: navbar, theme toggle, footer
│   ├── index.html            # Home: hero + merged About/Skills/Education
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
│   ├── js/
│   │   ├── theme-init.js    # Pre-paint light/dark detection (must be external — CSP blocks inline scripts)
│   │   ├── main.js          # CSRF handler + form submission + theme toggle
│   │   └── contact.js       # Turnstile callback
│   ├── images/               # .webp only
│   ├── favicon/
│   └── resume/
│
├── scripts/
│   ├── seed_projects.py     # Upsert-and-prune sync of portfolio projects (git is source of truth)
│   └── compress_images.py   # PNG/JPG -> WEBP, preserves real alpha transparency
│
└── tests/
    ├── conftest.py          # TestClient setup, fixtures, in-memory DB
    ├── test_routes.py       # Integration tests for all routes
    └── test_validators.py   # Unit tests for input validators
```

## Environment Variables
Copy `.env.example` and fill in:
- `DATABASE_URL` — PostgreSQL connection string (required; e.g. `postgresql://postgres:postgres@localhost:5433/portfolio`)
- `ADMIN_PASSWORD_HASH` — bcrypt hash of your admin password
- `JWT_SECRET` — strong random secret for token signing
- `CSRF_SECRET` — strong random secret for CSRF middleware
- `ENABLE_ADMIN` — set to `true` to enable the admin panel
- `RESEND_API_KEY` — Resend API key for email notifications
- `EMAIL_RECIPIENT` — your email for receiving contact form notifications
- `RECAPTCHA_SITE_KEY` — Cloudflare Turnstile site key
- `RECAPTCHA_SECRET_KEY` — Cloudflare Turnstile secret key

## Running Locally
1. Clone the repo
2. Create and activate a virtual environment
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in values
5. `alembic upgrade head` to set up the database
6. `python scripts/seed_projects.py` to seed projects
7. `python -m uvicorn main:app --reload --reload-exclude "*.log"` (excluding the log file prevents `--reload` from restarting the server — and re-running project sync on startup — every time a request gets logged)
8. Visit `http://localhost:8000`

## Running Tests
```bash
python -m pytest tests/ -v
```

## Deployment
Deployed on Railway. Connects to a Railway PostgreSQL database via `DATABASE_URL`.

## Status
Live.
