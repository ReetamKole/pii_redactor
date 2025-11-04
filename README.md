# PII Redaction Web App (FastAPI + GCP Cloud Storage)

A minimal starter that lets users upload a file + metadata.
The backend stores the raw file + JSON metadata to a GCS bucket,
runs regex-based PII redaction, and writes a processed copy to a second bucket.

