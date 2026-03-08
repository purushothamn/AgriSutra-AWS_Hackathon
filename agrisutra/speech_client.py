"""
Speech Client - Real Speech-to-Text Integration

This module provides speech-to-text functionality using AWS Transcribe.
"""

import boto3
import time
import uuid
from typing import Optional


class SpeechClient:
    """
    Speech-to-text client using AWS Transcribe.
    """
    
    def __init__(self, region_name: str = 'ap-south-1'):
        """
        Initialize the Speech client
        
        Args:
            region_name: AWS region (default: ap-south-1 for Mumbai)
        """
        try:
            self.transcribe_client = boto3.client('transcribe', region_name=region_name)
            self.s3_client = boto3.client('s3', region_name=region_name)
            self.region = region_name
            self.bucket_name = 'agrisutra-audio-temp'
        except Exception as e:
            print(f"Failed to initialize AWS clients: {e}")
            raise ValueError("AWS credentials not configured")
    
    def transcribe_audio(self, audio_bytes: bytes, language: str = "auto") -> Optional[str]:
        """
        Transcribe audio to text using AWS Transcribe.
        
        Args:
            audio_bytes: Audio data in bytes (WAV, MP3, etc.)
            language: Language hint (hi, kn, ta, en, or "auto")
        
        Returns:
            Transcribed text or None if failed
        """
        if not audio_bytes or len(audio_bytes) < 1024:
            return None
        
        try:
            # Convert language codes to AWS Transcribe format
            language_map = {
                "hi": "hi-IN",      # Hindi (India)
                "kn": "kn-IN",      # Kannada (India)
                "ta": "ta-IN",      # Tamil (India)
                "en": "en-IN",      # English (India)
                "auto": "en-IN"     # Default to English
            }
            
            aws_language = language_map.get(language, "en-IN")
            
            # Generate unique job name
            job_name = f"agrisutra-{uuid.uuid4().hex[:8]}"
            s3_key = f"audio/{job_name}.wav"
            
            # Upload audio to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=audio_bytes,
                ContentType='audio/wav'
            )
            
            media_uri = f"s3://{self.bucket_name}/{s3_key}"
            
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
                    
                    import requests
                    transcript_response = requests.get(transcript_uri)
                    transcript_data = transcript_response.json()
                    
                    transcribed_text = transcript_data['results']['transcripts'][0]['transcript']
                    
                    # Cleanup
                    self._cleanup(s3_key, job_name)
                    
                    return transcribed_text.strip() if transcribed_text else None
                
                elif job_status == 'FAILED':
                    self._cleanup(s3_key, job_name)
                    return None
                
                time.sleep(2)
                elapsed += 2
            
            # Timeout
            self._cleanup(s3_key, job_name)
            return None
                
        except Exception as e:
            print(f"Error calling AWS Transcribe: {str(e)}")
            return None
    
    def is_audio_valid(self, audio_bytes: bytes) -> bool:
        """
        Check if audio data is valid (not empty, has minimum length).
        
        Args:
            audio_bytes: Audio data in bytes
        
        Returns:
            True if audio seems valid, False otherwise
        """
        if not audio_bytes:
            return False
        
        # Check minimum size (at least 1KB for meaningful audio)
        if len(audio_bytes) < 1024:
            return False
        
        return True
    
    def _cleanup(self, s3_key: str, job_name: str):
        """Cleanup S3 objects and transcription jobs"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except Exception:
            pass
        
        try:
            self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
        except Exception:
            pass