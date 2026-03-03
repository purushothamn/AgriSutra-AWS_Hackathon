"""
Test TTS Integration

Quick test to verify text-to-speech functionality works correctly.
"""

from agrisutra.tts_client import TTSClient
from agrisutra.voice_pipeline import VoicePipeline

def test_tts_client():
    """Test TTS client directly"""
    print("Testing TTS Client...")
    
    tts = TTSClient()
    
    # Test English
    audio_en = tts.synthesize_speech("Hello farmer", "en")
    print(f"  English: {'✓' if audio_en else '✗'} ({len(audio_en) if audio_en else 0} bytes)")
    
    # Test Hindi
    audio_hi = tts.synthesize_speech("नमस्ते किसान", "hi")
    print(f"  Hindi: {'✓' if audio_hi else '✗'} ({len(audio_hi) if audio_hi else 0} bytes)")
    
    # Test Kannada
    audio_kn = tts.synthesize_speech("ನಮಸ್ಕಾರ ರೈತ", "kn")
    print(f"  Kannada: {'✓' if audio_kn else '✗'} ({len(audio_kn) if audio_kn else 0} bytes)")
    
    # Test Tamil
    audio_ta = tts.synthesize_speech("வணக்கம் விவசாயி", "ta")
    print(f"  Tamil: {'✓' if audio_ta else '✗'} ({len(audio_ta) if audio_ta else 0} bytes)")
    
    return all([audio_en, audio_hi, audio_kn, audio_ta])

def test_voice_pipeline():
    """Test voice pipeline with TTS"""
    print("\nTesting Voice Pipeline...")
    
    pipeline = VoicePipeline(use_mock=True)
    
    # Test synthesis through pipeline
    audio = pipeline.synthesize_speech("Weather is good today", "en")
    print(f"  Pipeline synthesis: {'✓' if audio else '✗'} ({len(audio) if audio else 0} bytes)")
    
    return audio is not None

if __name__ == "__main__":
    print("=" * 60)
    print("TTS Integration Test")
    print("=" * 60)
    
    try:
        tts_ok = test_tts_client()
        pipeline_ok = test_voice_pipeline()
        
        print("\n" + "=" * 60)
        if tts_ok and pipeline_ok:
            print("✅ All TTS tests passed!")
        else:
            print("❌ Some TTS tests failed")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
