# PowerShell deployment script
$PROJECT_ID = "pii-redactor-reetamkole"
$GCS_RAW_BUCKET = "pii-raw-reetamk"
$GCS_PROCESSED_BUCKET = "pii-processed-reetamk"
$DATABASE_URL = "postgresql://postgres:Redacter1!@34.93.219.152:5432/pii_redactor_db"
$IMAGE = "gcr.io/$PROJECT_ID/pii-redactor"

Write-Host "Authorizing external access to Cloud SQL..."
gcloud sql instances patch pii-redactor-instance --authorized-networks="0.0.0.0/0"

Write-Host "Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE

Write-Host "Deploying to Cloud Run..."
gcloud run deploy pii-redactor `
  --image $IMAGE `
  --platform managed `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars GCS_RAW_BUCKET=$GCS_RAW_BUCKET `
  --set-env-vars GCS_PROCESSED_BUCKET=$GCS_PROCESSED_BUCKET `
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID `
  --set-env-vars DATABASE_URL=$DATABASE_URL `
  --memory 1Gi `
  --cpu 1 `
  --max-instances 10

Write-Host "Deployment complete!"