

# PII Redactor Starter

A simple **FastAPI web app** to upload files, redact PII (emails, phone numbers) using regex, and store processed files locally or on Google Cloud.

---

## ⚙️ Setup

```bash
git clone https://github.com/reetamkole/pii_redactor_starter.git
cd pii_redactor_starter
python -m venv .venv
.venv\Scripts\activate   # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

