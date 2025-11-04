#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "Set PROJECT_ID env var"
  exit 1
fi

IMAGE="gcr.io/${PROJECT_ID}/pii-redactor"

gcloud builds submit --tag "${IMAGE}"
gcloud run deploy pii-redactor   --image "${IMAGE}"   --platform managed   --region asia-south1   --allow-unauthenticated   --set-env-vars GCS_RAW_BUCKET=${GCS_RAW_BUCKET:-your-raw-data-bucket}   --set-env-vars GCS_PROCESSED_BUCKET=${GCS_PROCESSED_BUCKET:-your-processed-data-bucket}   --set-env-vars PORT=8080
