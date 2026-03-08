"""
Intent Router - Query Classification and Agent Routing

This module implements the intent classification system that routes queries to specialized agents
based on keyword matching. It classifies queries into weather, finance, or general intents
and routes them to the appropriate agent.

Validates Requirements: 3.1, 3.2, 3.6
"""

import re
from enum import Enum
from typing import Dict, List


class Intent(Enum):
    """Query intent types for agent routing"""
    WEATHER = "weather"
    FINANCE = "finance"
    GENERAL = "general"


class IntentRouter:
    """
    Intent classification and routing system for AgriSutra queries.
    
    The router uses keyword matching to classify queries into weather, finance, or general
    intents, then routes them to the appropriate specialized agent.
    """
    
    def __init__(self):
        """Initialize the Intent Router with keyword dictionaries"""
        self._initialize_keywords()
    
    def _initialize_keywords(self):
        """Initialize keyword dictionaries for Hindi, Kannada, and Tamil"""
        # Weather-related keywords
        self.weather_keywords = {
            # English
            "weather", "rain", "rainfall", "temperature", "climate", "forecast",
            "storm", "wind", "humidity", "drought", "flood", "cyclone", "monsoon",
            "heat", "cold", "sunny", "cloudy", "disaster", "alert", "warning",
            
            # Hindi (Devanagari script)
            "मौसम", "बारिश", "वर्षा", "तापमान", "जलवायु", "पूर्वानुमान",
            "तूफान", "हवा", "आर्द्रता", "सूखा", "बाढ़", "चक्रवात", "मानसून",
            "गर्मी", "ठंड", "धूप", "बादल", "आपदा", "चेतावनी",
            
            # Kannada
            "ಹವಾಮಾನ", "ಮಳೆ", "ತಾಪಮಾನ", "ಹವಾಗುಣ", "ಮುನ್ಸೂಚನೆ",
            "ಚಂಡಮಾರುತ", "ಗಾಳಿ", "ತೇವಾಂಶ", "ಬರ", "ಪ್ರವಾಹ", "ಚಂಡಮಾರುತ", "ಮುಂಗಾರು",
            "ಬಿಸಿ", "ಚಳಿ", "ಬಿಸಿಲು", "ಮೋಡ", "ವಿಪತ್ತು", "ಎಚ್ಚರಿಕೆ",
            
            # Tamil
            "வானிலை", "மழை", "வெப்பநிலை", "காலநிலை", "முன்னறிவிப்பு",
            "புயல்", "காற்று", "ஈரப்பதம்", "வறட்சி", "வெள்ளம", "சூறாவளி", "பருவமழை",
            "வெப்பம்", "குளிர்", "வெயில்", "மேகம்", "பேரிடர்", "எச்சரிக்கை",
        }
        
        # Finance-related keywords
        self.finance_keywords = {
            # English
            "budget", "cost", "price", "money", "profit", "loss", "roi", "return",
            "investment", "expense", "income", "revenue", "market", "sell", "buy",
            "loan", "subsidy", "economics", "finance", "yield", "earning",
            
            # Hindi (Devanagari script)
            "बजट", "लागत", "कीमत", "पैसा", "लाभ", "हानि", "रिटर्न", "निवेश",
            "खर्च", "आय", "राजस्व", "बाजार", "बेचना", "खरीदना",
            "ऋण", "सब्सिडी", "अर्थशास्त्र", "वित्त", "उपज", "कमाई",
            
            # Kannada
            "ಬಜೆಟ್", "ವೆಚ್ಚ", "ಬೆಲೆ", "ಹಣ", "ಲಾಭ", "ನಷ್ಟ", "ರಿಟರ್ನ್", "ಹೂಡಿಕೆ",
            "ಖರ್ಚು", "ಆದಾಯ", "ಆದಾಯ", "ಮಾರುಕಟ್ಟೆ", "ಮಾರಾಟ", "ಖರೀದಿ",
            "ಸಾಲ", "ಸಬ್ಸಿಡಿ", "ಅರ್ಥಶಾಸ್ತ್ರ", "ಹಣಕಾಸು", "ಇಳುವರಿ", "ಗಳಿಕೆ",
            
            # Tamil
            "பட்ஜெட்", "செலவு", "விலை", "பணம்", "லாபம்", "நஷ்டம்", "வருமானம்", "முதலீடு",
            "செலவு", "வருமானம்", "வருவாய்", "சந்தை", "விற்பனை", "வாங்க",
            "கடன்", "மானியம்", "பொருளாதாரம்", "நிதி", "விளைச்சல்", "வருவாய்",
        }
    
    def classify_intent(self, query: str, language: str) -> Intent:
        """
        Classify query intent based on keyword matching.
        
        Args:
            query: User query text to classify
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Intent enum value (WEATHER, FINANCE, or GENERAL)
        
        Validates Requirements: 3.6
        """
        if not query:
            return Intent.GENERAL
        
        query_lower = query.lower()
        
        # Check for weather keywords
        weather_matches = 0
        for keyword in self.weather_keywords:
            keyword_lower = keyword.lower()
            # For ASCII keywords, use word boundary regex to avoid partial matches
            # For non-ASCII (Hindi, Kannada, Tamil), use simple substring matching
            if keyword_lower.isascii():
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, query_lower):
                    weather_matches += 1
            else:
                # For non-ASCII scripts, simple substring matching works better
                if keyword_lower in query_lower:
                    weather_matches += 1
        
        # Check for finance keywords
        finance_matches = 0
        for keyword in self.finance_keywords:
            keyword_lower = keyword.lower()
            # For ASCII keywords, use word boundary regex to avoid partial matches
            # For non-ASCII (Hindi, Kannada, Tamil), use simple substring matching
            if keyword_lower.isascii():
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, query_lower):
                    finance_matches += 1
            else:
                # For non-ASCII scripts, simple substring matching works better
                if keyword_lower in query_lower:
                    finance_matches += 1
        
        # Classify based on keyword matches
        if weather_matches > finance_matches and weather_matches > 0:
            return Intent.WEATHER
        elif finance_matches > weather_matches and finance_matches > 0:
            return Intent.FINANCE
        else:
            return Intent.GENERAL
    
    def route_to_agent(self, query: str, intent: Intent) -> str:
        """
        Route query to appropriate agent based on intent.
        
        Args:
            query: User query text
            intent: Classified intent (WEATHER, FINANCE, or GENERAL)
        
        Returns:
            Agent name string ("sentry", "economist", or "general")
        
        Validates Requirements: 3.1, 3.2
        """
        if intent == Intent.WEATHER:
            return "sentry"
        elif intent == Intent.FINANCE:
            return "economist"
        else:
            return "general"
