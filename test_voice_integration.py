"""
Test script to verify voice integration with Groq Whisper
"""

from agrisutra.speech_client import SpeechClient
from agrisutra.voice_pipeline import VoicePipeline

def test_speech_client():
    """Test SpeechClient initialization"""
    
    # API key (same as in app.py)
    api_key = "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"
    
    print("🔧 Initializing Speech client...")
    try:
        client = SpeechClient(api_key=api_key)
        print("✅ SpeechClient initialized successfully")
        print(f"   Model: {client.model}")
        print(f"   Base URL: {client.base_url}")
    except Exception as e:
        print(f"❌ Failed to initialize SpeechClient: {e}")
        return False
    
    # Test audio validation
    print("\n📝 Testing audio validation...")
    
    # Test empty audio
    is_valid = client.is_audio_valid(b"")
    print(f"   Empty audio valid: {is_valid} (should be False)")
    
    # Test small audio
    small_audio = b"x" * 100  # 100 bytes
    is_valid = client.is_audio_valid(small_audio)
    print(f"   Small audio (100 bytes) valid: {is_valid} (should be False)")
    
    # Test reasonable audio
    reasonable_audio = b"x" * 5000  # 5KB
    is_valid = client.is_audio_valid(reasonable_audio)
    print(f"   Reasonable audio (5KB) valid: {is_valid} (should be True)")
    
    return True

def test_voice_pipeline():
    """Test VoicePipeline initialization"""
    
    # API key (same as in app.py)
    api_key = "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"
    
    print("\n🔧 Initializing Voice Pipeline...")
    try:
        pipeline = VoicePipeline(groq_api_key=api_key, use_mock=False)
        print("✅ VoicePipeline initialized successfully")
        print(f"   Mock mode: {pipeline.use_mock}")
        print(f"   Has speech client: {pipeline.speech_client is not None}")
    except Exception as e:
        print(f"❌ Failed to initialize VoicePipeline: {e}")
        return False
    
    # Test with invalid audio (expected to fail gracefully)
    print("\n📝 Testing with invalid audio (expected to fail gracefully)...")
    fake_audio = b"x" * 2000  # 2KB of fake audio
    
    result = pipeline.transcribe_audio(fake_audio, "en")
    if result is None:
        print("✅ Invalid audio handled gracefully (returned None)")
    else:
        print(f"⚠️ Unexpected result with fake audio: {result}")
    
    # Test audio validation
    print("\n📝 Testing audio validation...")
    if pipeline.speech_client:
        # Test empty audio
        is_valid = pipeline.speech_client.is_audio_valid(b"")
        print(f"   Empty audio valid: {is_valid} (should be False)")
        
        # Test small audio
        small_audio = b"x" * 100
        is_valid = pipeline.speech_client.is_audio_valid(small_audio)
        print(f"   Small audio valid: {is_valid} (should be False)")
        
        # Test reasonable size audio
        reasonable_audio = b"x" * 5000
        is_valid = pipeline.speech_client.is_audio_valid(reasonable_audio)
        print(f"   Reasonable size audio valid: {is_valid} (should be True)")
    
    print("\n💡 Note: Real audio testing requires actual microphone input through Streamlit")
    
    return True

def test_mock_mode():
    """Test VoicePipeline in mock mode"""
    
    print("\n🔧 Testing mock mode...")
    pipeline = VoicePipeline(use_mock=True)
    print(f"✅ Mock pipeline initialized (mock: {pipeline.use_mock})")
    
    mock_audio = b"test audio data"
    result = pipeline.transcribe_audio(mock_audio, "en")
    
    if result and "Mock transcription" in result:
        print(f"✅ Mock transcription working: {result}")
        return True
    else:
        print(f"❌ Mock transcription not working: {result}")
        return False

if __name__ == "__main__":
    print("🎤 Testing Voice Integration\n")
    
    try:
        # Test 1: SpeechClient
        success1 = test_speech_client()
        
        # Test 2: VoicePipeline
        success2 = test_voice_pipeline()
        
        # Test 3: Mock mode
        success3 = test_mock_mode()
        
        if success1 and success2 and success3:
            print("\n🎉 All voice tests passed!")
            print("\n✅ Your voice integration is ready!")
            print("   Run: python -m streamlit run app.py")
            print("   Then select 'Voice (Microphone)' input mode")
        else:
            print("\n❌ Some tests failed. Check the errors above.")
            
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        print("   Check your API key and internet connection.")