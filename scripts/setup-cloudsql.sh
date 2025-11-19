#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "Set PROJECT_ID env var"
  exit 1
fi

REGION="asia-south1"
INSTANCE_NAME="pii-redactor-db"
DB_NAME="pii_redactor_db"
DB_USER="pii_user"

echo "Creating Cloud SQL instance..."
gcloud sql instances create ${INSTANCE_NAME} \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=${REGION} \
  --storage-type=SSD \
  --storage-size=10GB

echo "Creating database..."
gcloud sql databases create ${DB_NAME} \
  --instance=${INSTANCE_NAME}

echo "Creating user..."
gcloud sql users create ${DB_USER} \
  --instance=${INSTANCE_NAME} \
  --password="$(openssl rand -base64 32)"

echo "Setup complete!"
echo "INSTANCE_CONNECTION_NAME: ${PROJECT_ID}:${REGION}:${INSTANCE_NAME}"
echo "DB_NAME: ${DB_NAME}"
echo "DB_USER: ${DB_USER}"
echo "Note: Password was generated automatically. Check Cloud SQL console."