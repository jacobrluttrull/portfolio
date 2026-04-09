import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import AsyncMock, MagicMock, patch

# Set required env vars before importing the app
os.environ.setdefault("CSRF_SECRET", "a" * 64)
os.environ.setdefault("ENABLE_ADMIN", "true")
os.environ.setdefault("ADMIN_PASSWORD_HASH", "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW")  # bcrypt of "secret"
os.environ.setdefault("JWT_SECRET", "b" * 64)
os.environ.setdefault("RECAPTCHA_SECRET_KEY", "test_turnstile_secret")

from database import Base, get_db
from main import app

# In-memory SQLite for tests — isolated from the real portfolio.db
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


def _make_turnstile_mock(success: bool):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": success}
    mock_async_client = MagicMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=False)
    mock_async_client.post = AsyncMock(return_value=mock_response)
    return mock_async_client


@pytest.fixture
def turnstile_success():
    with patch("routers.pages.httpx.AsyncClient", return_value=_make_turnstile_mock(True)):
        yield


@pytest.fixture
def turnstile_fail():
    with patch("routers.pages.httpx.AsyncClient", return_value=_make_turnstile_mock(False)):
        yield


def get_csrf_token(client: TestClient) -> str:
    """Make a GET request to seed the CSRF cookie, then return the token value."""
    client.get("/contact")
    return client.cookies.get("csrftoken", "")
