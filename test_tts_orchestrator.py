"""
Test TTS with Orchestrator

Verify that the orchestrator generates audio responses correctly.
"""

from agrisutra.orchestrator import LambdaOrchestrator

def test_orchestrator_with_tts():
    """Test that orchestrator generates audio responses"""
    print("Testing Orchestrator with TTS...")
    
    # Initialize orchestrator with Groq API key
    groq_api_key = "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"
    orchestrator = LambdaOrchestrator(groq_api_key=groq_api_key)
    
    # Test with a simple text query in English
    event = {
        "input_type": "text",
        "input_data": "What is the weather in Bangalore?",
        "language": "en",
        "location": "bangalore"
    }
    
    print("\n  Processing query: 'What is the weather in Bangalore?'")
    response = orchestrator.handle_request(event)
    
    print(f"  Success: {response.success}")
    print(f"  Text response length: {len(response.text_response)} chars")
    print(f"  Audio response: {'✓' if response.audio_response else '✗'}")
    
    if response.audio_response:
        print(f"  Audio size: {len(response.audio_response):,} bytes ({len(response.audio_response)/1024:.1f} KB)")
    
    print(f"  Processing time: {response.processing_time_ms}ms")
    
    # Test with Hindi
    event_hindi = {
        "input_type": "text",
        "input_data": "बैंगलोर में मौसम कैसा है?",
        "language": "hi",
        "location": "bangalore"
    }
    
    print("\n  Processing Hindi query...")
    response_hindi = orchestrator.handle_request(event_hindi)
    
    print(f"  Success: {response_hindi.success}")
    print(f"  Audio response: {'✓' if response_hindi.audio_response else '✗'}")
    
    if response_hindi.audio_response:
        print(f"  Audio size: {len(response_hindi.audio_response):,} bytes ({len(response_hindi.audio_response)/1024:.1f} KB)")
    
    return response.success and response.audio_response is not None

if __name__ == "__main__":
    print("=" * 60)
    print("TTS Orchestrator Integration Test")
    print("=" * 60)
    
    try:
        success = test_orchestrator_with_tts()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ Orchestrator TTS integration working!")
        else:
            print("❌ Orchestrator TTS integration failed")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
