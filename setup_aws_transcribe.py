"""
AWS Transcribe Setup Helper Script

This script helps you set up AWS Transcribe for AgriSutra.
"""

import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("✅ AWS Credentials found!")
        print(f"   Account: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return True
    except NoCredentialsError:
        print("❌ No AWS credentials found!")
        print("\n📋 To configure AWS credentials, run:")
        print("   aws configure")
        print("\n   Or set environment variables:")
        print("   AWS_ACCESS_KEY_ID=your-access-key")
        print("   AWS_SECRET_ACCESS_KEY=your-secret-key")
        return False
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")
        return False

def check_s3_bucket(bucket_name='agrisutra-audio-temp', region='ap-south-1'):
    """Check if S3 bucket exists, create if not"""
    try:
        s3 = boto3.client('s3', region_name=region)
        
        # Check if bucket exists
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"✅ S3 bucket '{bucket_name}' exists!")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"⚠️  S3 bucket '{bucket_name}' not found. Creating...")
                
                # Create bucket
                if region == 'us-east-1':
                    s3.create_bucket(Bucket=bucket_name)
                else:
                    s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                
                print(f"✅ Created S3 bucket '{bucket_name}'!")
                return True
            else:
                print(f"❌ Error accessing bucket: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error with S3: {e}")
        return False

def check_transcribe_access(region='ap-south-1'):
    """Check if Transcribe service is accessible"""
    try:
        transcribe = boto3.client('transcribe', region_name=region)
        
        # Try to list transcription jobs (will fail if no permissions)
        transcribe.list_transcription_jobs(MaxResults=1)
        
        print(f"✅ AWS Transcribe access confirmed in {region}!")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print(f"❌ No permission to access AWS Transcribe!")
            print("\n📋 Required IAM permissions:")
            print("   - transcribe:StartTranscriptionJob")
            print("   - transcribe:GetTranscriptionJob")
            print("   - transcribe:DeleteTranscriptionJob")
            print("   - transcribe:ListTranscriptionJobs")
        else:
            print(f"❌ Error accessing Transcribe: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error with Transcribe: {e}")
        return False

def test_transcribe_workflow(bucket_name='agrisutra-audio-temp', region='ap-south-1'):
    """Test the complete transcribe workflow"""
    print("\n🧪 Testing AWS Transcribe workflow...")
    
    try:
        import uuid
        import time
        
        s3 = boto3.client('s3', region_name=region)
        transcribe = boto3.client('transcribe', region_name=region)
        
        # Create a small test audio file (silence)
        test_audio = b'\x00' * 2048  # 2KB of silence
        test_key = f"test/test-{uuid.uuid4().hex[:8]}.wav"
        job_name = f"test-{uuid.uuid4().hex[:8]}"
        
        print(f"   Uploading test audio to S3...")
        s3.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_audio,
            ContentType='audio/wav'
        )
        
        print(f"   Starting test transcription job...")
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f"s3://{bucket_name}/{test_key}"},
            MediaFormat='wav',
            LanguageCode='en-IN'
        )
        
        print(f"   Waiting for job to complete...")
        max_wait = 30
        elapsed = 0
        
        while elapsed < max_wait:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            
            if job_status in ['COMPLETED', 'FAILED']:
                break
            
            time.sleep(2)
            elapsed += 2
        
        # Cleanup
        print(f"   Cleaning up test resources...")
        try:
            s3.delete_object(Bucket=bucket_name, Key=test_key)
            transcribe.delete_transcription_job(TranscriptionJobName=job_name)
        except:
            pass
        
        if job_status == 'COMPLETED':
            print("✅ AWS Transcribe workflow test PASSED!")
            return True
        else:
            print(f"⚠️  Test job status: {job_status}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("🎤 AWS Transcribe Setup for AgriSutra")
    print("=" * 60)
    print()
    
    # Step 1: Check credentials
    print("Step 1: Checking AWS Credentials...")
    if not check_aws_credentials():
        print("\n❌ Setup failed: No AWS credentials")
        return False
    print()
    
    # Step 2: Check/Create S3 bucket
    print("Step 2: Checking S3 Bucket...")
    if not check_s3_bucket():
        print("\n❌ Setup failed: S3 bucket issue")
        return False
    print()
    
    # Step 3: Check Transcribe access
    print("Step 3: Checking AWS Transcribe Access...")
    if not check_transcribe_access():
        print("\n❌ Setup failed: No Transcribe access")
        return False
    print()
    
    # Step 4: Test workflow
    print("Step 4: Testing Complete Workflow...")
    if not test_transcribe_workflow():
        print("\n⚠️  Workflow test had issues, but basic setup is complete")
    print()
    
    print("=" * 60)
    print("✅ AWS Transcribe Setup Complete!")
    print("=" * 60)
    print("\n🚀 You can now run: streamlit run app.py")
    print()
    
    return True

if __name__ == "__main__":
    main()
