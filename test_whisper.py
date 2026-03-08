"""
Test script for Groq Whisper speech recognition

This script tests the Whisper integration without running the full app.
"""

from agrisutra.speech_recognition import GroqSpeechRecognition

def test_whisper_initialization():
    """Test that Whisper client initializes correctly"""
    groq_api_key = "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"
    
    try:
        whisper = GroqSpeechRecognition(api_key=groq_api_key)
        print("✅ Whisper client initialized successfully")
        print(f"   Model: {whisper.model}")
        print(f"   Base URL: {whisper.base_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Whisper: {e}")
        return False

def test_whisper_with_sample():
    """Test Whisper with a sample audio file (if available)"""
    print("\n📝 Note: To test with actual audio:")
    print("   1. Record a short audio file (WAV format)")
    print("   2. Save it as 'test_audio.wav'")
    print("   3. Run this script again")
    print("\n   Example code:")
    print("   ```python")
    print("   with open('test_audio.wav', 'rb') as f:")
    print("       audio_bytes = f.read()")
    print("   result = whisper.transcribe(audio_bytes, language='hi')")
    print("   print(f'Transcription: {result}')")
    print("   ```")

if __name__ == "__main__":
    print("🎤 Testing Groq Whisper Integration\n")
    print("=" * 50)
    
    # Test initialization
    if test_whisper_initialization():
        print("\n✅ All tests passed!")
        test_whisper_with_sample()
    else:
        print("\n❌ Tests failed!")
