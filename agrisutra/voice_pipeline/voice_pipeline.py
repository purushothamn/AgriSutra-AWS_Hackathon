"""
Voice Pipeline - Real Speech Processing

This module implements the voice input/output pipeline using AWS Transcribe for
speech-to-text and gTTS for text-to-speech functionality.

Validates Requirements: 2.1, 2.2, 2.3, 2.5
"""

import time
from typing import Optional
from agrisutra.speech_client import SpeechClient
from agrisutra.tts_client import TTSClient


class VoicePipeline:
    """
    Voice Pipeline for multilingual speech-to-text and text-to-speech.
    
    Uses Groq's Whisper for audio transcription and gTTS for speech synthesis
    in Hindi, Kannada, Tamil, and English languages.
    """
    
    def __init__(self, groq_api_key: str = None, use_mock: bool = False):
        """
        Initialize the Voice Pipeline
        
        Args:
            groq_api_key: Groq API key for LLM (not used for speech anymore)
            use_mock: If True, use mock mode instead of real services
        """
        self.use_mock = use_mock
        
        # Initialize speech-to-text client (now uses AWS)
        if not use_mock:
            try:
                self.speech_client = SpeechClient(region_name='ap-south-1')
            except Exception as e:
                print(f"AWS speech client initialization failed: {e}")
                # Fall back to mock mode if AWS client fails
                self.use_mock = True
                self.speech_client = None
        else:
            self.speech_client = None
            self.use_mock = True
        
        # Initialize text-to-speech client (always available)
        try:
            self.tts_client = TTSClient()
        except Exception as e:
            print(f"TTS client initialization failed: {e}")
            self.tts_client = None
    
    def transcribe_audio(self, audio_bytes: bytes, language: str) -> Optional[str]:
        """
        Transcribe audio to text using AWS Transcribe.
        
        Args:
            audio_bytes: Audio data in bytes (WAV format)
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Transcribed text string or None if transcription fails
        
        Validates Requirements: 2.3
        """
        if not audio_bytes:
            return None
        
        # Use mock mode for testing
        if self.use_mock:
            return f"[Mock transcription for {language} audio - {len(audio_bytes)} bytes]"
        
        if not self.speech_client:
            return None
        
        # Check if audio is valid
        if not self.speech_client.is_audio_valid(audio_bytes):
            return None
        
        try:
            # Use AWS Transcribe API for transcription
            transcribed_text = self.speech_client.transcribe_audio(audio_bytes, language)
            
            if transcribed_text:
                # Clean up the transcription
                transcribed_text = transcribed_text.strip()
                
                # Basic validation - ensure it's not just noise
                if len(transcribed_text) > 2:  # At least a few characters
                    return transcribed_text
            
            return None
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return None
    
    def synthesize_speech(self, text: str, language: str) -> Optional[bytes]:
        """
        Synthesize speech from text using gTTS.
        
        Args:
            text: Text to synthesize
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Audio data in bytes (MP3 format) or None if synthesis fails
        
        Validates Requirements: 2.5
        """
        if not text:
            return None
        
        # Use TTS client if available
        if self.tts_client:
            try:
                return self.tts_client.synthesize_speech(text, language)
            except Exception as e:
                print(f"TTS synthesis error: {e}")
                return None
        
        return None
    
    def process_voice_input(self, audio_bytes: bytes, language: str) -> Optional[str]:
        """
        Process voice input: transcribe audio to text.
        
        This is a convenience method that wraps transcribe_audio with error handling.
        
        Args:
            audio_bytes: Audio data in bytes
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Transcribed text or None if processing fails
        
        Validates Requirements: 2.1, 2.2, 2.3
        """
        return self.transcribe_audio(audio_bytes, language)
    
    def process_voice_output(self, text: str, language: str) -> Optional[bytes]:
        """
        Process voice output: synthesize text to speech.
        
        This is a convenience method that wraps synthesize_speech with error handling.
        
        Args:
            text: Text to synthesize
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Audio data in bytes or None if processing fails
        
        Validates Requirements: 2.5
        """
        return self.synthesize_speech(text, language)
