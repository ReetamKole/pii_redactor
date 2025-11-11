import re

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

DOB_RE = re.compile(r"\b(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")

CC_RE_FLEX = re.compile(r"\b(?:\d[ -]?){13,19}\b")

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

MASTER = re.compile(
    rf"""(
        (?P<email>{EMAIL_RE.pattern})
      | (?P<ssn>{SSN_RE.pattern})
      | (?P<dob>{DOB_RE.pattern})
      | (?P<cc>{CC_RE_FLEX.pattern})
      | (?P<phone>{PHONE_RE.pattern})
    )""",
    re.VERBOSE,
)

def redact_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    def repl(m: re.Match) -> str:
        g = m.groupdict()

        
        if g.get("email"):
            return "[REDACTED_EMAIL]"

     
        if g.get("ssn") or g.get("dob") or g.get("cc"):
            return m.group(0)

     
        if g.get("phone"):
            return "[REDACTED_PHONE]"

        return m.group(0)

    return MASTER.sub(repl, text)


def is_valid_phone(phone: str) -> bool:
    if not isinstance(phone, str):
        return False
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15
