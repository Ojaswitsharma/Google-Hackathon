# Deploy script for Windows PowerShell

# Set your project configuration
$PROJECT_ID = "your-google-cloud-project-id"
$FUNCTION_NAME = "merge-media-files"
$REGION = "us-central1"
$RAW_ASSETS_BUCKET = "your-raw-assets-bucket-name"
$OUTPUT_BUCKET = "your-output-bucket-name"

# Deploy the Cloud Function
gcloud functions deploy $FUNCTION_NAME `
    --gen2 `
    --runtime=python311 `
    --region=$REGION `
    --source=. `
    --entry-point=merge_media_files `
    --trigger-bucket=$RAW_ASSETS_BUCKET `
    --set-env-vars RAW_ASSETS_BUCKET=$RAW_ASSETS_BUCKET,OUTPUT_BUCKET=$OUTPUT_BUCKET `
    --memory=1GB `
    --timeout=540s `
    --project=$PROJECT_ID

Write-Host "Deployment complete!"
Write-Host "Function Name: $FUNCTION_NAME"
Write-Host "Trigger Bucket: $RAW_ASSETS_BUCKET"
Write-Host "Output Bucket: $OUTPUT_BUCKET"
