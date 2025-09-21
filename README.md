# Media File Merger - Google Cloud Function

This project automatically merges video, audio, and description files when they are uploaded to a Google Cloud Storage bucket.

## How it works

1. **Input Files**: Your friends upload three files with a shared unique ID:
   - `projectX_video.mp4` (or other video formats)
   - `projectX_audio.mp3` (or other audio formats)  
   - `projectX_description.json` (contains description text)

2. **Automatic Trigger**: When any file is uploaded to the raw-assets bucket, the Cloud Function is triggered

3. **File Check**: The function checks if all three files for the project ID are present

4. **Merging Process**: If all files are present, the function:
   - Downloads the video and audio files
   - Reads the description from the JSON file
   - Uses FFmpeg to merge the video and audio
   - Overlays the description as subtitles on the video
   - Uploads the final merged video to the output bucket

## Features

- **Automatic Detection**: Detects when all required files are uploaded
- **Video Overlay**: Description text is overlaid as subtitles on the video
- **Multiple Formats**: Supports various video and audio formats
- **Error Handling**: Comprehensive error handling and logging
- **Scalable**: Runs on Google Cloud Functions for automatic scaling

## File Structure

```
d:\Google-Hakathon\
├── main.py              # Main Cloud Function code
├── requirements.txt     # Python dependencies
├── app.yaml            # Cloud Function configuration
├── deploy.sh           # Linux/Mac deployment script
├── deploy.ps1          # Windows PowerShell deployment script
├── test_main.py        # Unit tests
└── README.md           # This file
```

## Setup Instructions

### Prerequisites

1. Google Cloud Project with billing enabled
2. Google Cloud SDK (gcloud) installed
3. Cloud Functions API enabled
4. Cloud Storage API enabled
5. Two Cloud Storage buckets:
   - Raw assets bucket (for input files)
   - Output bucket (for merged videos)

### Python Virtual Environment Setup

1. Create and activate a virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

### Configuration

1. Edit the deployment script (`deploy.ps1` for Windows):
   - Set your `PROJECT_ID`
   - Set your `RAW_ASSETS_BUCKET` name
   - Set your `OUTPUT_BUCKET` name
   - Adjust `REGION` if needed

2. Update `app.yaml` with your bucket names

### Deployment

Run the deployment script:
```powershell
.\deploy.ps1
```

Or deploy manually:
```powershell
gcloud functions deploy merge-media-files `
    --gen2 `
    --runtime=python311 `
    --region=us-central1 `
    --source=. `
    --entry-point=merge_media_files `
    --trigger-bucket=your-raw-assets-bucket-name `
    --set-env-vars RAW_ASSETS_BUCKET=your-raw-assets-bucket-name,OUTPUT_BUCKET=your-output-bucket-name `
    --memory=1GB `
    --timeout=540s
```

## Input File Format

### Description JSON Format
```json
{
  "description": "This is the description text that will be overlaid on the video. It can be multiple sentences and will be automatically formatted as subtitles.",
  "project_id": "projectX",
  "created_at": "2025-09-10T10:00:00Z"
}
```

### File Naming Convention
- Video: `{project_id}_video.{extension}` (e.g., `projectX_video.mp4`)
- Audio: `{project_id}_audio.{extension}` (e.g., `projectX_audio.mp3`)
- Description: `{project_id}_description.json`

## Output

The merged video will be uploaded to the output bucket with the name:
`{project_id}_final.mp4`

## Testing

Run the unit tests:
```powershell
python -m pytest test_main.py -v
```

Or using unittest:
```powershell
python test_main.py
```

## FFmpeg Integration

The function uses FFmpeg to:
- Merge video and audio streams
- Add subtitle overlay with description text
- Encode the final video in MP4 format with H.264 codec

## Monitoring

Monitor the function through:
- Google Cloud Console > Cloud Functions
- Cloud Logging for detailed logs
- Cloud Storage for uploaded files

## Troubleshooting

1. **Function not triggering**: Check bucket permissions and trigger configuration
2. **FFmpeg errors**: Ensure input files are valid media files
3. **Memory issues**: Increase memory allocation in deployment script
4. **Timeout issues**: Increase timeout value for large files

## Environment Variables

- `RAW_ASSETS_BUCKET`: Name of the input bucket
- `OUTPUT_BUCKET`: Name of the output bucket

## Supported File Formats

### Video
- MP4, AVI, MOV, MKV

### Audio  
- MP3, WAV, AAC, M4A

### Description
- JSON format only
