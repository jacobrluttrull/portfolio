import pytest
from tests.conftest import get_csrf_token


# --- Public GET routes ---

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200

def test_projects_page(client):
    response = client.get("/projects")
    assert response.status_code == 200

def test_contact_page(client):
    response = client.get("/contact")
    assert response.status_code == 200

def test_contact_success_message(client):
    response = client.get("/contact?success=true")
    assert response.status_code == 200
    assert "Message sent successfully" in response.text

def test_contact_no_success_on_other_params(client):
    response = client.get("/contact?success=yes")
    assert "Message sent successfully" not in response.text

def test_404_page(client):
    response = client.get("/nonexistent-page")
    assert response.status_code == 404


# --- Contact form POST ---

VALID_FORM = {
    "name": "John Smith",
    "email": "john@example.com",
    "subject": "Job Opportunity",
    "message": "Hello, I would like to get in touch with you about a backend role.",
    "cf-turnstile-response": "test-token",
}

def test_contact_submit_valid(client, turnstile_success):
    csrf = get_csrf_token(client)
    response = client.post("/contact", data=VALID_FORM, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "success=true" in str(response.url)

def test_contact_submit_with_phone(client, turnstile_success):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "phone_number": "+1 555 123 4567"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "success=true" in str(response.url)

def test_contact_invalid_name(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "name": "A"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "Name must be between" in response.text

def test_contact_invalid_email(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "email": "not-an-email"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "valid email" in response.text

def test_contact_invalid_subject(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "subject": "A"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "Subject must be" in response.text

def test_contact_message_too_short(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "message": "Hi"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "at least 10 characters" in response.text

def test_contact_invalid_phone(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "phone_number": "abc"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "Phone must be" in response.text

def test_contact_xss_attempt_rejected(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "name": "<script>alert(1)</script>"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "Name must be between" in response.text

def test_contact_turnstile_failure(client, turnstile_fail):
    csrf = get_csrf_token(client)
    response = client.post("/contact", data=VALID_FORM, headers={"x-csrftoken": csrf})
    assert response.status_code == 200
    assert "Verification failed" in response.text

def test_contact_preserves_values_on_error(client):
    csrf = get_csrf_token(client)
    data = {**VALID_FORM, "email": "bad-email"}
    response = client.post("/contact", data=data, headers={"x-csrftoken": csrf})
    assert "John Smith" in response.text


# --- Admin auth wall ---

def test_admin_dashboard_requires_auth(client):
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 302
    assert "/admin/login" in response.headers["location"]

def test_admin_add_requires_auth(client):
    response = client.get("/admin/add", follow_redirects=False)
    assert response.status_code == 302

def test_admin_login_page_accessible(client):
    response = client.get("/admin/login")
    assert response.status_code == 200

def test_admin_login_wrong_password(client):
    csrf = get_csrf_token(client)
    response = client.post(
        "/admin/login",
        data={"password": "wrongpassword"},
        headers={"x-csrftoken": csrf}
    )
    assert response.status_code == 200
    assert "Invalid password" in response.text
