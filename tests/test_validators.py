import pytest
from utils.validators import (
    sanitize,
    validate_name,
    validate_email,
    validate_subject,
    validate_phone,
    validate_message,
    validate_url,
)


# --- sanitize ---

def test_sanitize_escapes_html():
    assert sanitize("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"

def test_sanitize_escapes_ampersand():
    assert sanitize("Tom & Jerry") == "Tom &amp; Jerry"

def test_sanitize_plain_text_unchanged():
    assert sanitize("Hello World") == "Hello World"


# --- validate_name ---

def test_name_valid():
    assert validate_name("Jacob") is True

def test_name_with_hyphen():
    assert validate_name("Mary-Jane") is True

def test_name_with_spaces():
    assert validate_name("John Smith") is True

def test_name_too_short():
    assert validate_name("A") is False

def test_name_minimum_length():
    assert validate_name("Jo") is True

def test_name_maximum_length():
    assert validate_name("A" * 65) is True

def test_name_too_long():
    assert validate_name("A" * 66) is False

def test_name_special_chars():
    assert validate_name("Jacob<script>") is False

def test_name_empty():
    assert validate_name("") is False

def test_name_whitespace_only():
    assert validate_name("   ") is False


# --- validate_email ---

def test_email_valid():
    assert validate_email("user@example.com") is True

def test_email_valid_subdomain():
    assert validate_email("user@mail.example.co.uk") is True

def test_email_valid_plus():
    assert validate_email("user+tag@example.com") is True

def test_email_missing_at():
    assert validate_email("userexample.com") is False

def test_email_missing_domain():
    assert validate_email("user@") is False

def test_email_missing_tld():
    assert validate_email("user@example") is False

def test_email_double_at():
    assert validate_email("user@@example.com") is False

def test_email_too_long():
    assert validate_email("a" * 95 + "@b.com") is False

def test_email_empty():
    assert validate_email("") is False


# --- validate_subject ---

def test_subject_valid():
    assert validate_subject("Job Opportunity") is True

def test_subject_with_punctuation():
    assert validate_subject("Hello, how are you?") is True

def test_subject_too_short():
    assert validate_subject("A") is False

def test_subject_minimum_length():
    assert validate_subject("Hi") is True

def test_subject_too_long():
    assert validate_subject("A" * 201) is False

def test_subject_disallowed_chars():
    assert validate_subject("<script>") is False

def test_subject_empty():
    assert validate_subject("") is False


# --- validate_phone ---

def test_phone_us_format():
    assert validate_phone("(555) 123-4567") is True

def test_phone_international():
    assert validate_phone("+1 800 555 0199") is True

def test_phone_digits_only():
    assert validate_phone("5551234567") is True

def test_phone_too_short():
    assert validate_phone("123") is False

def test_phone_too_long():
    assert validate_phone("1" * 21) is False

def test_phone_letters():
    assert validate_phone("555-CALL-ME") is False

def test_phone_minimum_length():
    assert validate_phone("1234567") is True


# --- validate_message ---

def test_message_valid():
    assert validate_message("Hello, I would like to get in touch with you.") is True

def test_message_too_short():
    assert validate_message("Hi") is False

def test_message_minimum_length():
    assert validate_message("A" * 10) is True

def test_message_maximum_length():
    assert validate_message("A" * 2000) is True

def test_message_too_long():
    assert validate_message("A" * 2001) is False

def test_message_empty():
    assert validate_message("") is False

def test_message_whitespace_only():
    assert validate_message("          ") is False


# --- validate_url ---

def test_url_full_https():
    assert validate_url("https://github.com/user/repo") is True

def test_url_no_protocol():
    assert validate_url("github.com/user/repo") is True

def test_url_static_path():
    assert validate_url("/static/images/project.png") is True

def test_url_http():
    assert validate_url("http://example.com") is True

def test_url_invalid():
    assert validate_url("not a url!!!") is False

def test_url_javascript_scheme():
    assert validate_url("javascript:alert(1)") is False

def test_url_empty():
    assert validate_url("") is False
