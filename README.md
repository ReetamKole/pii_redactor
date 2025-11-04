# PII Redaction Web App (FastAPI + GCP Cloud Storage)

A minimal starter that lets users upload a file + metadata.
The backend stores the raw file + JSON metadata to a GCS bucket,
runs regex-based PII redaction, and writes a processed copy to a second bucket.

## 1) Prereqs
- Python 3.11+
- A GCP Project with billing enabled
- Two GCS buckets:
  - RAW bucket (e.g., `my-pii-raw`)
  - PROCESSED bucket (e.g., `my-pii-processed`)
- A Service Account with roles:
  - Storage Object Admin
  - Storage Legacy Bucket Writer (optional)
- Service Account key JSON on your machine

## 2) Local setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env to set GOOGLE_APPLICATION_CREDENTIALS and bucket names
```

## 3) Run locally
```bash
uvicorn app.main:app --reload --port 8080
```

Open http://127.0.0.1:8080 and upload a CSV/TXT.

## 4) Docker
```bash
docker build -t pii-redactor:local .
docker run -it --rm -p 8080:8080 --env-file .env -v /abs/path/service-account.json:/sa.json pii-redactor:local
# Inside .env set GOOGLE_APPLICATION_CREDENTIALS=/sa.json
```

## 5) Deploy to Cloud Run (manual)
Make sure `gcloud` is installed and authenticated.
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/pii-redactor
gcloud run deploy pii-redactor   --image gcr.io/PROJECT_ID/pii-redactor   --platform managed   --region asia-south1   --allow-unauthenticated   --set-env-vars GCS_RAW_BUCKET=your-raw-data-bucket,GCS_PROCESSED_BUCKET=your-processed-data-bucket   --set-env-vars PORT=8080
# Then add a Secret/Var for GOOGLE_APPLICATION_CREDENTIALS or use Workload Identity (recommended)
```

## 6) Tests
```bash
pytest -q
```
