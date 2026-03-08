"""
AWS Speech Recognition using AWS Transcribe

This module provides speech-to-text functionality using AWS Transcribe service.
"""

import boto3
import time
import uuid
from typing import Optional
import io


class AWSSpeechRecognition:
    """
    Speech recognition client using AWS Transcribe.
    Supports real-time and batch transcription for Indian languages.
    """
    
    def __init__(
        self, 
        region_name: str = 'ap-south-1', 
        bucket_name: str = 'agrisutra-audio-temp',
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ):
        """
        Initialize the AWS Transcribe client
        
        Args:
            region_name: AWS region (default: ap-south-1 for Mumbai)
            bucket_name: S3 bucket name for temporary audio storage
            aws_access_key_id: AWS access key (optional, uses default credentials if not provided)
            aws_secret_access_key: AWS secret key (optional, uses default credentials if not provided)
        """
        try:
            # Create session with credentials if provided
            if aws_access_key_id and aws_secret_access_key:
                session = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                )
                self.transcribe_client = session.client('transcribe')
                self.s3_client = session.client('s3')
            else:
                # Use default credentials
                self.transcribe_client = boto3.client('transcribe', region_name=region_name)
                self.s3_client = boto3.client('s3', region_name=region_name)
            
            self.region = region_name
            self.bucket_name = bucket_name
            
            # Don't check bucket during initialization - will check when needed
            print(f"✅ AWS Transcribe initialized with bucket: {bucket_name}")
            
        except Exception as e:
            print(f"Failed to initialize AWS clients: {e}")
            raise ValueError(f"AWS Transcribe initialization failed: {e}")
    
    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> Optional[str]:
        """
        Transcribe audio to text using AWS Transcribe.
        
        Args:
            audio_bytes: Audio data in bytes (WAV, MP3, M4A, etc.)
            language: Optional language code (hi, kn, ta, en) for better accuracy
        
        Returns:
            Transcribed text or None if transcription fails
        """
        if not audio_bytes or len(audio_bytes) < 1024:
            print("Audio too short or empty")
            return None
        
        try:
            # Map language codes to AWS Transcribe language codes
            language_map = {
                'hi': 'hi-IN',  # Hindi (India)
                'kn': 'kn-IN',  # Kannada (India)
                'ta': 'ta-IN',  # Tamil (India)
                'en': 'en-IN'   # English (India)
            }
            
            aws_language = language_map.get(language, 'en-IN')
            
            # Generate unique job name
            job_name = f"agrisutra-{uuid.uuid4().hex[:8]}"
            s3_key = f"audio/{job_name}.wav"
            
            print(f"Uploading audio to S3: s3://{self.bucket_name}/{s3_key}")
            
            # Upload audio to S3
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=audio_bytes,
                    ContentType='audio/wav'
                )
            except Exception as s3_error:
                print(f"S3 upload failed: {s3_error}")
                print(f"⚠️  Check if your AWS user has s3:PutObject permission on bucket '{self.bucket_name}'")
                return None
            
            media_uri = f"s3://{self.bucket_name}/{s3_key}"
            
            print(f"Starting transcription job: {job_name}")
            
            # Start transcription job
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': media_uri},
                MediaFormat='wav',
                LanguageCode=aws_language
            )
            
            # Wait for completion (max 30 seconds)
            max_wait = 30
            elapsed = 0
            
            while elapsed < max_wait:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                
                job_status = status['TranscriptionJob']['TranscriptionJobStatus']
                
                if job_status == 'COMPLETED':
                    # Get transcript
                    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    
                    print(f"Transcription completed, fetching results...")
                    
                    import requests
                    transcript_response = requests.get(transcript_uri)
                    transcript_data = transcript_response.json()
                    
                    transcribed_text = transcript_data['results']['transcripts'][0]['transcript']
                    
                    # Cleanup
                    self._cleanup(s3_key, job_name)
                    
                    print(f"Transcription successful: {transcribed_text}")
                    return transcribed_text.strip() if transcribed_text else None
                
                elif job_status == 'FAILED':
                    failure_reason = status['TranscriptionJob'].get('FailureReason', 'Unknown')
                    print(f"Transcription failed: {failure_reason}")
                    self._cleanup(s3_key, job_name)
                    return None
                
                time.sleep(2)
                elapsed += 2
            
            # Timeout
            print(f"Transcription timed out after {max_wait} seconds")
            self._cleanup(s3_key, job_name)
            return None
                
        except Exception as e:
            print(f"Error calling AWS Transcribe: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _cleanup(self, s3_key: str, job_name: str):
        """Cleanup S3 objects and transcription jobs"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"Deleted S3 object: {s3_key}")
        except Exception as e:
            print(f"Failed to delete S3 object: {e}")
        
        try:
            self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
            print(f"Deleted transcription job: {job_name}")
        except Exception as e:
            print(f"Failed to delete transcription job: {e}")
