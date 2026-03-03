"""
Debug script to test the complete orchestrator flow
"""

from agrisutra.orchestrator import LambdaOrchestrator

def test_orchestrator_weather_query():
    """Test the complete orchestrator flow for weather query"""
    
    print("🔍 Testing complete orchestrator flow...")
    
    # Initialize orchestrator
    api_key = "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"
    orchestrator = LambdaOrchestrator(groq_api_key=api_key)
    
    # Test event (same format as app.py)
    event = {
        "input_type": "text",
        "input_data": "how is weather in bangalore",
        "language": "hi",  # Hindi language (like user's case)
        "location": "bangalore",
        "crop": "rice",
        "area": 1.0
    }
    
    print(f"\n📝 Event: {event}")
    
    # Process request
    print("\n🔄 Processing request...")
    response = orchestrator.handle_request(event)
    
    print(f"\n📊 Response:")
    print(f"   Success: {response.success}")
    print(f"   Text: {response.text_response}")
    print(f"   Error: {response.error_message}")
    print(f"   Processing time: {response.processing_time_ms}ms")
    
    # Check if response is appropriate
    if response.success:
        if "नमस्ते" in response.text_response and "मौसम" not in response.text_response:
            print("\n⚠️ ISSUE: Getting generic greeting instead of weather response")
            return False
        elif "मौसम" in response.text_response or "बैंगलोर" in response.text_response:
            print("\n✅ Response looks appropriate for weather query")
            return True
        else:
            print("\n⚠️ Response doesn't seem weather-related")
            return False
    else:
        print(f"\n❌ Request failed: {response.error_message}")
        return False

def test_english_weather_query():
    """Test with English language"""
    
    print("\n🔍 Testing English weather query...")
    
    api_key = "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"
    orchestrator = LambdaOrchestrator(groq_api_key=api_key)
    
    event = {
        "input_type": "text",
        "input_data": "how is weather in bangalore",
        "language": "en",  # English language
        "location": "bangalore",
        "crop": "rice",
        "area": 1.0
    }
    
    response = orchestrator.handle_request(event)
    
    print(f"\n📊 English Response:")
    print(f"   Success: {response.success}")
    print(f"   Text: {response.text_response}")
    
    return response.success

if __name__ == "__main__":
    try:
        print("🧪 Testing Orchestrator Flow for Weather Queries\n")
        
        # Test Hindi (user's case)
        hindi_success = test_orchestrator_weather_query()
        
        # Test English for comparison
        english_success = test_english_weather_query()
        
        if hindi_success and english_success:
            print("\n🎉 Both tests passed!")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"\n❌ Debug error: {str(e)}")
        import traceback
        traceback.print_exc()