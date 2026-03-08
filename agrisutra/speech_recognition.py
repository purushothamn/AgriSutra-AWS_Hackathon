"""
Speech Recognition using Groq Whisper API

This module provides speech-to-text functionality using Groq's Whisper API.
"""

import requests
from typing import Optional
import io


class GroqSpeechRecognition:
    """
    Speech recognition client using Groq's Whisper API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the speech recognition client
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "whisper-large-v3-turbo"  # Fast Whisper model
    
    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> Optional[str]:
        """
        Transcribe audio to text using Groq Whisper API.
        
        Args:
            audio_bytes: Audio data in bytes (WAV, MP3, M4A, etc.)
            language: Optional language code (hi, kn, ta, en) for better accuracy
        
        Returns:
            Transcribed text or None if transcription fails
        """
        if not audio_bytes:
            return None
        
        try:
            # Prepare the file for upload
            files = {
                'file': ('audio.wav', io.BytesIO(audio_bytes), 'audio/wav')
            }
            
            data = {
                'model': self.model,
                'response_format': 'text'
            }
            
            # Add language hint if provided
            if language:
                # Map our language codes to Whisper language codes
                language_map = {
                    'hi': 'hi',  # Hindi
                    'kn': 'kn',  # Kannada
                    'ta': 'ta',  # Tamil
                    'en': 'en'   # English
                }
                whisper_lang = language_map.get(language, 'en')
                data['language'] = whisper_lang
            
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.post(
                f"{self.base_url}/audio/transcriptions",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                # Response is plain text
                transcribed_text = response.text.strip()
                return transcribed_text if transcribed_text else None
            else:
                print(f"Groq Whisper API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None
