# AWS Transcribe Setup Guide

AgriSutra now uses AWS Transcribe for speech-to-text, which provides better support for Indian languages (Hindi, Kannada, Tamil, English).

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI configured with credentials
3. S3 bucket for temporary audio storage

## Setup Steps

### 1. Configure AWS Credentials

Create or update `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Create or update `~/.aws/config`:

```ini
[default]
region = ap-south-1
```

### 2. Create S3 Bucket for Audio Storage

```bash
aws s3 mb s3://agrisutra-audio-temp --region ap-south-1
```

### 3. Set IAM Permissions

Your AWS user/role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::agrisutra-audio-temp/*"
    }
  ]
}
```

### 4. Update Configuration (Optional)

If you want to use a different S3 bucket or region, update `agrisutra/speech_recognition.py`:

```python
# Change bucket name
bucket_name = 'your-bucket-name'

# Change region in orchestrator.py
self.speech_recognition = AWSSpeechRecognition(region_name='your-region')
```

## Supported Languages

AWS Transcribe supports these language codes:
- `hi-IN` - Hindi (India)
- `kn-IN` - Kannada (India)
- `ta-IN` - Tamil (India)
- `en-IN` - English (India)

## Cost Considerations

AWS Transcribe pricing (as of 2024):
- Standard: $0.024 per minute (first 250 million minutes per month)
- For a 30-second query: ~$0.012

For 1000 queries/month: ~$12/month

## Testing

Test the setup:

```bash
python -c "
from agrisutra.speech_recognition import AWSSpeechRecognition
import wave

# Create test audio
sr = AWSSpeechRecognition()
print('AWS Transcribe client initialized successfully!')
"
```

## Troubleshooting

### Error: "NoCredentialsError"
- Run `aws configure` to set up credentials
- Verify credentials file exists at `~/.aws/credentials`

### Error: "NoSuchBucket"
- Create the S3 bucket: `aws s3 mb s3://agrisutra-audio-temp`
- Verify bucket name matches in code

### Error: "AccessDenied"
- Check IAM permissions for Transcribe and S3
- Ensure your user/role has the required policies

### Slow transcription
- AWS Transcribe typically takes 2-5 seconds for short audio
- Consider using AWS Transcribe Streaming API for real-time transcription

## Alternative: AWS Transcribe Streaming

For real-time transcription with lower latency, consider using AWS Transcribe Streaming API. This requires WebSocket connection and is more complex but provides instant results.

See: https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html

## Production Recommendations

1. Use AWS Transcribe Streaming API for real-time transcription
2. Implement audio compression before upload to reduce costs
3. Set up S3 lifecycle policies to auto-delete old audio files
4. Use CloudWatch to monitor transcription job metrics
5. Implement retry logic with exponential backoff
6. Consider caching common queries to reduce API calls
