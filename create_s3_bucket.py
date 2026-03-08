"""
Create S3 bucket for AgriSutra audio storage
"""

import boto3
from botocore.exceptions import ClientError

# Your AWS credentials
AWS_ACCESS_KEY_ID = "AKIA44QOQ7WEC6YRG3UX"
AWS_SECRET_ACCESS_KEY = "fLNEUzLFU5tnnyGNS/dHB4+v51rzpT4VMAtoNLkm"
REGION = "ap-south-1"
BUCKET_NAME = "agrisutra-audio-temp"

def create_bucket():
    """Create S3 bucket if it doesn't exist"""
    try:
        # Create session with credentials
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION
        )
        
        s3_client = session.client('s3')
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=BUCKET_NAME)
            print(f"✅ S3 bucket '{BUCKET_NAME}' already exists!")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"Creating S3 bucket '{BUCKET_NAME}'...")
                
                # Create bucket
                s3_client.create_bucket(
                    Bucket=BUCKET_NAME,
                    CreateBucketConfiguration={'LocationConstraint': REGION}
                )
                
                print(f"✅ Created S3 bucket '{BUCKET_NAME}' successfully!")
                return True
            else:
                print(f"❌ Error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Failed to create bucket: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🪣 Creating S3 Bucket for AgriSutra")
    print("=" * 60)
    print()
    
    if create_bucket():
        print()
        print("=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print("\n🚀 You can now run: streamlit run app.py")
    else:
        print("\n❌ Setup failed. Please check your AWS credentials.")
