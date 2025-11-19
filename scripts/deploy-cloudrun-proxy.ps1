# PowerShell deployment script for Cloud SQL Proxy
$PROJECT_ID = "pii-redactor-reetamkole"
$GCS_RAW_BUCKET = "pii-raw-reetamk"
$GCS_PROCESSED_BUCKET = "pii-processed-reetamk"
$INSTANCE_CONNECTION_NAME = "pii-redactor-reetamkole:asia-south1:pii-redactor-instance"
$DATABASE_URL = "postgresql://postgres:Redacter1!@/cloudsql/$INSTANCE_CONNECTION_NAME/pii_redactor_db"
$IMAGE = "gcr.io/$PROJECT_ID/pii-redactor"

Write-Host "Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE

Write-Host "Deploying to Cloud Run with Cloud SQL Proxy..."
gcloud run deploy pii-redactor `
  --image $IMAGE `
  --platform managed `
  --region asia-south1 `
  --allow-unauthenticated `
  --add-cloudsql-instances $INSTANCE_CONNECTION_NAME `
  --set-env-vars GCS_RAW_BUCKET=$GCS_RAW_BUCKET `
  --set-env-vars GCS_PROCESSED_BUCKET=$GCS_PROCESSED_BUCKET `
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID `
  --set-env-vars DATABASE_URL=$DATABASE_URL `
  --memory 1Gi `
  --cpu 1 `
  --max-instances 10

Write-Host "Deployment complete!"