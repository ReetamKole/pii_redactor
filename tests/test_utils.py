from app.utils import redact_text, is_valid_phone

def test_redact_email():
    s = "Contact me at test@example.com"
    assert "[REDACTED_EMAIL]" in redact_text(s)

def test_redact_phone():
    s = "My number is +91-98765-43210"
    assert "[REDACTED_PHONE]" in redact_text(s)

def test_is_valid_phone():
    assert is_valid_phone("+91 9876543210")
    assert not is_valid_phone("123")
