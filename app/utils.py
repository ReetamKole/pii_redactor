import re

EMAIL_RE = re.compile(
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    re.IGNORECASE
)

PHONE_RE = re.compile(
    r"""
    (?<!\d)                             
    (?:\+?\d{1,3}[\s\-.]?)?             
    (?:\(?\d{2,4}\)?[\s\-.]?)?          
    (?:\d[\s\-.]?){6,14}\d              
    (?!\d)                              
    """,
    re.VERBOSE,
)

def redact_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text

def is_valid_phone(phone: str) -> bool:
    if not isinstance(phone, str):
        return False
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 7 <= len(digits) <= 15