import re

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?\d[\s-]?){7,15}")

def redact_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text

def is_valid_phone(phone: str) -> bool:
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 10 <= len(digits) <= 15
