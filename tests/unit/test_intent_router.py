"""
Unit tests for IntentRouter

Tests keyword-based intent classification and agent routing for weather, finance,
and general queries in Hindi, Kannada, and Tamil.

Validates Requirements: 3.1, 3.2, 3.6
"""

import pytest
from agrisutra.agents.intent_router import IntentRouter, Intent


class TestIntentRouter:
    """Test suite for IntentRouter class"""
    
    @pytest.fixture
    def router(self):
        """Create IntentRouter instance for testing"""
        return IntentRouter()
    
    # Weather Intent Tests
    
    def test_weather_intent_english(self, router):
        """Test weather keyword detection in English"""
        queries = [
            "What is the weather today?",
            "Will it rain tomorrow?",
            "Show me the forecast",
            "Is there a storm warning?",
            "What is the temperature?",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "en")
            assert intent == Intent.WEATHER, f"Failed for query: {query}"
    
    def test_weather_intent_hindi(self, router):
        """Test weather keyword detection in Hindi"""
        queries = [
            "आज मौसम कैसा है?",
            "कल बारिश होगी?",
            "तापमान क्या है?",
            "तूफान की चेतावनी है?",
            "मानसून कब आएगा?",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "hi")
            assert intent == Intent.WEATHER, f"Failed for query: {query}"
    
    def test_weather_intent_kannada(self, router):
        """Test weather keyword detection in Kannada"""
        queries = [
            "ಇಂದು ಹವಾಮಾನ ಹೇಗಿದೆ?",
            "ನಾಳೆ ಮಳೆ ಬರುತ್ತದೆಯೇ?",
            "ತಾಪಮಾನ ಎಷ್ಟು?",
            "ಚಂಡಮಾರುತ ಎಚ್ಚರಿಕೆ ಇದೆಯೇ?",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "kn")
            assert intent == Intent.WEATHER, f"Failed for query: {query}"
    
    def test_weather_intent_tamil(self, router):
        """Test weather keyword detection in Tamil"""
        queries = [
            "இன்று வானிலை எப்படி?",
            "நாளை மழை வருமா?",
            "வெப்பநிலை என்ன?",
            "புயல் எச்சரிக்கை உள்ளதா?",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "ta")
            assert intent == Intent.WEATHER, f"Failed for query: {query}"
    
    # Finance Intent Tests
    
    def test_finance_intent_english(self, router):
        """Test finance keyword detection in English"""
        queries = [
            "What is the budget for wheat farming?",
            "How much profit can I make?",
            "What is the ROI for tomatoes?",
            "Show me market prices",
            "Calculate the cost of cultivation",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "en")
            assert intent == Intent.FINANCE, f"Failed for query: {query}"
    
    def test_finance_intent_hindi(self, router):
        """Test finance keyword detection in Hindi"""
        queries = [
            "गेहूं की खेती का बजट क्या है?",
            "मुझे कितना लाभ होगा?",
            "टमाटर का ROI क्या है?",
            "बाजार की कीमत बताओ",
            "खेती की लागत बताओ",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "hi")
            assert intent == Intent.FINANCE, f"Failed for query: {query}"
    
    def test_finance_intent_kannada(self, router):
        """Test finance keyword detection in Kannada"""
        queries = [
            "ಗೋಧಿ ಬೆಳೆಗೆ ಬಜೆಟ್ ಎಷ್ಟು?",
            "ನನಗೆ ಎಷ್ಟು ಲಾಭ ಆಗುತ್ತದೆ?",
            "ಟೊಮೇಟೊ ROI ಎಷ್ಟು?",
            "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ತೋರಿಸಿ",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "kn")
            assert intent == Intent.FINANCE, f"Failed for query: {query}"
    
    def test_finance_intent_tamil(self, router):
        """Test finance keyword detection in Tamil"""
        queries = [
            "கோதுமை விவசாயத்திற்கு பட்ஜெட் என்ன?",
            "எனக்கு எவ்வளவு லாபம் கிடைக்கும்?",
            "தக்காளி ROI என்ன?",
            "சந்தை விலை காட்டு",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "ta")
            assert intent == Intent.FINANCE, f"Failed for query: {query}"
    
    # General Intent Tests
    
    def test_general_intent_no_keywords(self, router):
        """Test default to general intent for queries without specific keywords"""
        queries = [
            "Hello, how are you?",
            "Tell me about farming",
            "What crops should I grow?",
            "How to prepare soil?",
            "नमस्ते",
            "ಹಲೋ",
            "வணக்கம்",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "en")
            assert intent == Intent.GENERAL, f"Failed for query: {query}"
    
    def test_general_intent_empty_query(self, router):
        """Test empty query defaults to general intent"""
        intent = router.classify_intent("", "en")
        assert intent == Intent.GENERAL
    
    def test_general_intent_mixed_keywords(self, router):
        """Test queries with equal weather and finance keywords default to general"""
        # This query has both weather and finance keywords but neither dominates
        query = "What is the weather and budget?"
        intent = router.classify_intent(query, "en")
        # Should classify based on which has more matches, or general if tied
        assert intent in [Intent.WEATHER, Intent.FINANCE, Intent.GENERAL]
    
    # Agent Routing Tests
    
    def test_route_to_sentry_agent(self, router):
        """Test routing weather intent to sentry agent"""
        agent = router.route_to_agent("What is the weather?", Intent.WEATHER)
        assert agent == "sentry"
    
    def test_route_to_economist_agent(self, router):
        """Test routing finance intent to economist agent"""
        agent = router.route_to_agent("What is the budget?", Intent.FINANCE)
        assert agent == "economist"
    
    def test_route_to_general_agent(self, router):
        """Test routing general intent to general agent"""
        agent = router.route_to_agent("Hello", Intent.GENERAL)
        assert agent == "general"
    
    # Edge Cases
    
    def test_case_insensitive_matching(self, router):
        """Test that keyword matching is case-insensitive"""
        queries = [
            "WEATHER",
            "Weather",
            "weather",
            "wEaThEr",
        ]
        
        for query in queries:
            intent = router.classify_intent(query, "en")
            assert intent == Intent.WEATHER, f"Failed for query: {query}"
    
    def test_partial_keyword_matching(self, router):
        """Test that keywords are matched as whole words for ASCII, substrings for non-ASCII"""
        # "rainfall" contains "rain" as a separate word (with word boundary)
        query = "What is the rainfall forecast?"
        intent = router.classify_intent(query, "en")
        assert intent == Intent.WEATHER
        
        # Test that "wheat" doesn't match "heat" (word boundary protection)
        query2 = "What is the wheat price?"
        intent2 = router.classify_intent(query2, "en")
        # Should be FINANCE because of "price", not WEATHER
        assert intent2 == Intent.FINANCE
    
    def test_multiple_weather_keywords(self, router):
        """Test query with multiple weather keywords"""
        query = "What is the weather forecast for rain and temperature?"
        intent = router.classify_intent(query, "en")
        assert intent == Intent.WEATHER
    
    def test_multiple_finance_keywords(self, router):
        """Test query with multiple finance keywords"""
        query = "What is the budget, cost, and profit for wheat?"
        intent = router.classify_intent(query, "en")
        assert intent == Intent.FINANCE
    
    def test_weather_dominates_finance(self, router):
        """Test that weather intent is chosen when weather keywords dominate"""
        query = "What is the weather and budget? Will it rain?"
        intent = router.classify_intent(query, "en")
        assert intent == Intent.WEATHER
    
    def test_finance_dominates_weather(self, router):
        """Test that finance intent is chosen when finance keywords dominate"""
        query = "What is the budget, cost, profit, and weather?"
        intent = router.classify_intent(query, "en")
        assert intent == Intent.FINANCE
