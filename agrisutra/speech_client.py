"""
Speech Client - Real Speech-to-Text Integration

This module provides speech-to-text functionality using Groq's Whisper API.
"""

import io
import requests
from typing import Optional


class SpeechClient:
    """
    Speech-to-text client using Groq's Whisper API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Speech client
        
        Args:
            api_key: Groq API key (same as for LLM)
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "whisper-large-v3-turbo"  # Fast Whisper model
    
    def transcribe_audio(self, audio_bytes: bytes, language: str = "auto") -> Optional[str]:
        """
        Transcribe audio to text using Groq's Whisper API.
        
        Args:
            audio_bytes: Audio data in bytes (WAV, MP3, etc.)
            language: Language hint (hi, kn, ta, en, or "auto")
        
        Returns:
            Transcribed text or None if failed
        """
        if not audio_bytes:
            return None
        
        try:
            # Convert language codes to Whisper format
            language_map = {
                "hi": "hi",      # Hindi
                "kn": "kn",      # Kannada  
                "ta": "ta",      # Tamil
                "en": "en",      # English
                "auto": None     # Let Whisper auto-detect
            }
            
            whisper_language = language_map.get(language, None)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Prepare the audio file
            files = {
                "file": ("audio.wav", io.BytesIO(audio_bytes), "audio/wav"),
                "model": (None, self.model),
                "response_format": (None, "text")
            }
            
            # Add language if specified
            if whisper_language:
                files["language"] = (None, whisper_language)
            
            response = requests.post(
                f"{self.base_url}/audio/transcriptions",
                headers=headers,
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                # Whisper returns plain text when response_format is "text"
                transcribed_text = response.text.strip()
                
                if transcribed_text:
                    return transcribed_text
                else:
                    return None
            else:
                print(f"Whisper API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Whisper API: {str(e)}")
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