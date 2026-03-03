"""
Text-to-Speech Client - Voice Output

This module provides text-to-speech functionality using gTTS (Google Text-to-Speech).
"""

from gtts import gTTS
import io
from typing import Optional


class TTSClient:
    """
    Text-to-Speech client using Google TTS.
    Supports Hindi, Kannada, Tamil, and English.
    """
    
    def __init__(self):
        """Initialize the TTS client"""
        # Language mapping for gTTS
        self.language_map = {
            "hi": "hi",  # Hindi
            "kn": "kn",  # Kannada
            "ta": "ta",  # Tamil
            "en": "en"   # English
        }
    
    def synthesize_speech(self, text: str, language: str = "en") -> Optional[bytes]:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to convert to speech
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Audio data in bytes (MP3 format) or None if failed
        """
        if not text or len(text.strip()) == 0:
            return None
        
        try:
            # Get gTTS language code
            tts_lang = self.language_map.get(language, "en")
            
            # Create TTS object
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Return audio bytes
            return audio_buffer.read()
            
        except Exception as e:
            print(f"TTS error: {str(e)}")
            return None
    
    def is_language_supported(self, language: str) -> bool:
        """
        Check if a language is supported.
        
        Args:
            language: Language code to check
        
        Returns:
            True if supported, False otherwise
        """
        return language in self.language_map
