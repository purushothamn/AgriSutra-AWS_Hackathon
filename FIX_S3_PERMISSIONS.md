# Fix S3 Bucket Permissions

## ❌ Current Issue
Your AWS user `AgriSutra-Streamlit` doesn't have permission to access the bucket `agrisutra-general`.

## ✅ Solution Options

### **Option 1: Ask AWS Administrator (Recommended)**

Send this to your AWS administrator:

```
Hi,

I need access to the S3 bucket for AgriSutra voice transcription.

AWS User: arn:aws:iam::885867478408:user/AgriSutra-Streamlit
S3 Bucket: agrisutra-general
Region: ap-south-1

Required Permissions:
- s3:PutObject (to upload audio files)
- s3:GetObject (to read audio files)
- s3:DeleteObject (to clean up after transcription)
- transcribe:StartTranscriptionJob
- transcribe:GetTranscriptionJob  
- transcribe:DeleteTranscriptionJob

Please add these permissions to my user or create a policy that allows access to this bucket.

Thank you!
```

### **Option 2: IAM Policy (For Administrator)**

If you have admin access, attach this policy to the `AgriSutra-Streamlit` user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::agrisutra-general/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::agrisutra-general"
    },
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob",
        "transcribe:ListTranscriptionJobs"
      ],
      "Resource": "*"
    }
  ]
}
```

### **Option 3: Use Different Bucket**

If you have access to another S3 bucket, update `app.py`:

```python
aws_bucket_name = "your-accessible-bucket-name"  # Change this
```

### **Option 4: Create New Bucket (If You Have Permission)**

If you have `s3:CreateBucket` permission:

```bash
aws s3 mb s3://agrisutra-streamlit-audio --region ap-south-1
```

Then update `app.py`:
```python
aws_bucket_name = "agrisutra-streamlit-audio"
```

## 🧪 Test Permissions

After permissions are fixed, test with:

```bash
streamlit run app.py
```

You should see:
- ✅ "Groq LLM + AWS Transcribe connected!"
- Voice input should work without errors

## 📋 Current Status

- ✅ AWS credentials are valid
- ✅ Transcribe service is accessible
- ❌ S3 bucket `agrisutra-general` - Access Denied
- ⏳ Waiting for S3 permissions

## 🔧 Temporary Workaround

The app will now start even without S3 access, but voice input won't work until permissions are fixed. You can still use text input for testing.
