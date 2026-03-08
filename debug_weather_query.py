"""
Debug script to test weather query processing
"""

from agrisutra.agents.intent_router import IntentRouter
from agrisutra.agents.sentry_agent import SentryAgent
from agrisutra.groq_client import GroqClient
from agrisutra.config import get_system_prompt

def test_weather_query_processing():
    """Test the complete weather query processing pipeline"""
    
    print("🔍 Debugging weather query processing...")
    
    # Test query
    query = "how is weather in bangalore"
    language = "en"
    location = "bangalore"
    
    print(f"\n📝 Query: '{query}'")
    print(f"📍 Location: '{location}'")
    print(f"🌐 Language: '{language}'")
    
    # Step 1: Test intent classification
    print("\n1️⃣ Testing Intent Classification...")
    intent_router = IntentRouter()
    intent = intent_router.classify_intent(query, language)
    agent_name = intent_router.route_to_agent(query, intent)
    
    print(f"   Intent: {intent}")
    print(f"   Agent: {agent_name}")
    
    # Step 2: Test weather agent
    print("\n2️⃣ Testing Weather Agent...")
    sentry_agent = SentryAgent()
    weather_data = sentry_agent.fetch_weather_data(location)
    
    if weather_data:
        print(f"   ✅ Weather data retrieved:")
        print(f"      Temperature: {weather_data.temperature_celsius}°C")
        print(f"      Humidity: {weather_data.humidity_percent}%")
        print(f"      Rainfall: {weather_data.rainfall_mm}mm")
        print(f"      Wind: {weather_data.wind_speed_kmh} km/h")
        
        # Check for disaster conditions
        is_disaster = sentry_agent.detect_disaster_conditions(weather_data)
        print(f"      Disaster conditions: {is_disaster}")
    else:
        print("   ❌ No weather data retrieved")
        return False
    
    # Step 3: Test context building
    print("\n3️⃣ Testing Context Building...")
    if agent_name == "sentry" and weather_data:
        agent_context = f"\n\nWeather Context for {location}: Temperature {weather_data.temperature_celsius}°C, Humidity {weather_data.humidity_percent}%, Rainfall {weather_data.rainfall_mm}mm, Wind {weather_data.wind_speed_kmh} km/h."
        if sentry_agent.detect_disaster_conditions(weather_data):
            agent_context += " WARNING: Disaster conditions detected!"
        
        print(f"   ✅ Context built:")
        print(f"      {agent_context}")
    else:
        print("   ❌ No context built")
        agent_context = ""
    
    # Step 4: Test LLM query
    print("\n4️⃣ Testing LLM Query...")
    enriched_query = query + agent_context
    system_prompt = get_system_prompt(language)
    
    print(f"   System prompt: {system_prompt[:100]}...")
    print(f"   Enriched query: {enriched_query}")
    
    # Test with Groq client
    api_key = "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"
    groq_client = GroqClient(api_key=api_key)
    
    try:
        response = groq_client.generate_response(enriched_query, language, system_prompt)
        if response:
            print(f"   ✅ LLM Response received:")
            print(f"      {response[:200]}...")
            
            # Check if response is relevant to weather
            if any(word in response.lower() for word in ["weather", "temperature", "bangalore", "climate"]):
                print("   ✅ Response seems relevant to weather query")
                return True
            else:
                print("   ⚠️ Response doesn't seem weather-related")
                print(f"   Full response: {response}")
                return False
        else:
            print("   ❌ No LLM response received")
            return False
    except Exception as e:
        print(f"   ❌ LLM error: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = test_weather_query_processing()
        if success:
            print("\n🎉 Weather query processing is working correctly!")
        else:
            print("\n❌ Issues found in weather query processing.")
            print("   Check the steps above to identify the problem.")
    except Exception as e:
        print(f"\n❌ Debug error: {str(e)}")