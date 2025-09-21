# Example configuration file for local testing
import os

# Set environment variables for local testing
os.environ['RAW_ASSETS_BUCKET'] = 'your-raw-assets-bucket'
os.environ['OUTPUT_BUCKET'] = 'your-output-bucket'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-key.json'
