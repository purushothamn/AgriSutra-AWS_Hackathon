"""
Debug script to test Hindi weather query processing
"""

from agrisutra.agents.intent_router import IntentRouter
from agrisutra.agents.sentry_agent import SentryAgent
from agrisutra.groq_client import GroqClient
from agrisutra.config import get_system_prompt

def test_hindi_weather_query():
    """Test weather query in Hindi"""
    
    print("🔍 Testing Hindi weather query...")
    
    # Test with Hindi language setting
    query = "how is weather in bangalore"  # English query
    language = "hi"  # Hindi language setting
    location = "bangalore"
    
    print(f"\n📝 Query: '{query}'")
    print(f"🌐 Language setting: '{language}' (Hindi)")
    
    # Get system prompt for Hindi
    system_prompt = get_system_prompt(language)
    print(f"\n📋 System prompt for Hindi:")
    print(f"   {system_prompt}")
    
    # Test LLM with Hindi system prompt
    api_key = "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"
    groq_client = GroqClient(api_key=api_key)
    
    # Add weather context
    sentry_agent = SentryAgent()
    weather_data = sentry_agent.fetch_weather_data(location)
    
    if weather_data:
        agent_context = f"\n\nWeather Context for {location}: Temperature {weather_data.temperature_celsius}°C, Humidity {weather_data.humidity_percent}%, Rainfall {weather_data.rainfall_mm}mm, Wind {weather_data.wind_speed_kmh} km/h."
        enriched_query = query + agent_context
    else:
        enriched_query = query
    
    print(f"\n🔄 Enriched query: {enriched_query}")
    
    try:
        response = groq_client.generate_response(enriched_query, language, system_prompt)
        if response:
            print(f"\n✅ LLM Response:")
            print(f"   {response}")
            
            # Check if it's a generic greeting vs weather response
            if "नमस्ते" in response and "मौसम" not in response:
                print("\n⚠️ ISSUE FOUND: Getting generic greeting instead of weather response")
                return False
            else:
                print("\n✅ Response looks appropriate")
                return True
        else:
            print("\n❌ No response received")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_english_vs_hindi():
    """Compare English vs Hindi responses"""
    
    print("\n🔄 Comparing English vs Hindi responses...")
    
    query = "how is weather in bangalore"
    api_key = "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"
    groq_client = GroqClient(api_key=api_key)
    
    # Get weather context
    sentry_agent = SentryAgent()
    weather_data = sentry_agent.fetch_weather_data("bangalore")
    agent_context = f"\n\nWeather Context for bangalore: Temperature {weather_data.temperature_celsius}°C, Humidity {weather_data.humidity_percent}%, Rainfall {weather_data.rainfall_mm}mm, Wind {weather_data.wind_speed_kmh} km/h."
    enriched_query = query + agent_context
    
    # Test English
    print("\n🇺🇸 English Response:")
    en_prompt = get_system_prompt("en")
    en_response = groq_client.generate_response(enriched_query, "en", en_prompt)
    print(f"   {en_response[:200]}...")
    
    # Test Hindi
    print("\n🇮🇳 Hindi Response:")
    hi_prompt = get_system_prompt("hi")
    hi_response = groq_client.generate_response(enriched_query, "hi", hi_prompt)
    print(f"   {hi_response[:200]}...")
    
    return True

if __name__ == "__main__":
    try:
        test_hindi_weather_query()
        test_english_vs_hindi()
    except Exception as e:
        print(f"\n❌ Debug error: {str(e)}")