from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
import dotenv
from starlette_csrf import CSRFMiddleware
from utils.logger import get_logger
from scripts.seed_projects import seed_projects
dotenv.load_dotenv()
CSRF_SECRET = os.getenv("CSRF_SECRET")
if not CSRF_SECRET:
    raise ValueError("CSRF_SECRET environment variable is not set.")


from routers import pages, admin

seed_projects()
app = FastAPI()





logger = get_logger(__name__)
logger.info("Portfolio app starting up...")

templates = Jinja2Templates(directory="templates")

app.add_middleware(CSRFMiddleware, secret=CSRF_SECRET)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response




@app.exception_handler(StarletteHTTPException)
async def custom_http_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    if exc.headers and "Location" in exc.headers:
        return RedirectResponse(url=exc.headers["Location"], status_code=exc.status_code)
    raise exc

app.mount("/static", StaticFiles(directory="static"), name="static")
if os.getenv("ENABLE_ADMIN") == "true":
    app.include_router(admin.router)
app.include_router(pages.router)
