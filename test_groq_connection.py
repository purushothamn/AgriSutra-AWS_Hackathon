"""
Quick test script to verify Groq API connection
"""

from agrisutra.groq_client import GroqClient

def test_groq_connection():
    """Test Groq API connection with a simple query"""
    
    # API key (same as in app.py)
    api_key = "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"
    
    print("🔧 Initializing Groq client...")
    client = GroqClient(api_key=api_key)
    print("✅ Client initialized successfully")
    
    print("\n📝 Testing English query...")
    response_en = client.generate_response(
        prompt="What is crop rotation?",
        language="en"
    )
    
    if response_en:
        print("✅ English response received:")
        print(f"   {response_en[:100]}...")
    else:
        print("❌ Failed to get English response")
        return False
    
    print("\n📝 Testing Hindi query...")
    response_hi = client.generate_response(
        prompt="फसल चक्र क्या है?",
        language="hi"
    )
    
    if response_hi:
        print("✅ Hindi response received:")
        print(f"   {response_hi[:100]}...")
    else:
        print("❌ Failed to get Hindi response")
        return False
    
    print("\n🎉 All tests passed! Groq integration is working correctly.")
    return True

if __name__ == "__main__":
    try:
        success = test_groq_connection()
        if success:
            print("\n✅ Your AgriSutra is ready to use!")
            print("   Run: python -m streamlit run app.py")
        else:
            print("\n❌ Some tests failed. Check your API key and internet connection.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("   Check your API key and internet connection.")
