"""
Resilience Sentry - Safety Governance Layer

This module implements the safety validation layer that prevents harmful agricultural advice
by detecting banned keywords in queries and responses, and returning localized safety messages.

Validates Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
"""

import re
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of safety validation check"""
    is_safe: bool
    blocked_keywords: List[str]
    safety_message: Optional[str]


class ResilienceSentry:
    """
    Safety governance layer that validates queries and responses to prevent harmful agricultural advice.
    
    The sentry maintains banned keyword patterns in multiple languages (Hindi, Kannada, Tamil)
    and provides localized safety messages when unsafe content is detected.
    """
    
    def __init__(self):
        """Initialize the Resilience Sentry with banned keyword patterns"""
        self._initialize_banned_patterns()
        self._initialize_safety_messages()
    
    def _initialize_banned_patterns(self):
        """Initialize banned keyword patterns for chemical mixing and unsafe practices"""
        # Banned patterns for chemical mixing
        self.banned_patterns = {
            # Chemical mixing patterns
            "chemical_mixing": [
                # English
                r"mix\s+pesticide",
                r"combine\s+pesticide",
                r"mix\s+chemical",
                r"combine\s+chemical",
                r"mix\s+insecticide",
                # Hindi (Devanagari script)
                r"कीटनाशक\s+मिला",
                r"कीटनाशक\s+मिक्स",
                r"रसायन\s+मिला",
                r"कीटनाशक.*मिला",
                # Kannada
                r"ಕೀಟನಾಶಕ\s+ಮಿಶ್ರಣ",
                r"ಕೀಟನಾಶಕ.*ಮಿಶ್ರಿಸ",
                r"ರಾಸಾಯನಿಕ.*ಮಿಶ್ರಣ",
                # Tamil
                r"பூச்சிக்கொல்லி.*கலக்க",
                r"பூச்சிக்கொல்லி.*கலவை",
                r"இரசாயன.*கலக்க",
            ],
            
            # Unsafe agricultural practices
            "unsafe_practices": [
                # English
                r"burn\s+crop",
                r"burn\s+stubble",
                r"set\s+fire",
                # Hindi
                r"फसल\s+जला",
                r"पराली\s+जला",
                r"आग\s+लगा",
                r"फसल.*जला",
                # Kannada
                r"ಬೆಳೆ\s+ಸುಡು",
                r"ಬೆಳೆ.*ಸುಡು",
                r"ಬೆಂಕಿ\s+ಹಚ್ಚು",
                # Tamil
                r"பயிர்.*எரி",
                r"தீ.*வை",
            ],
            
            # Ignoring safety warnings
            "ignore_warnings": [
                # English
                r"ignore\s+warning",
                r"skip\s+safety",
                r"bypass\s+precaution",
                # Hindi
                r"चेतावनी\s+अनदेखा",
                r"चेतावनी.*नजरअंदाज",
                r"सावधानी.*छोड़",
                # Kannada
                r"ಎಚ್ಚರಿಕೆ\s+ನಿರ್ಲಕ್ಷಿಸ",
                r"ಎಚ್ಚರಿಕೆ.*ನಿರ್ಲಕ್ಷ",
                # Tamil
                r"எச்சரிக்கை.*புறக்கணி",
                r"எச்சரிக்கை.*தவிர்",
            ],
        }
    
    def _initialize_safety_messages(self):
        """Initialize localized safety messages for each supported language"""
        self.safety_messages = {
            "hi": "यह सलाह सुरक्षित नहीं है। कृपया अन्य प्रश्न पूछें या कृषि विशेषज्ञ से परामर्श करें।",
            "kn": "ಈ ಸಲಹೆ ಸುರಕ್ಷಿತವಲ್ಲ. ದಯವಿಟ್ಟು ಬೇರೆ ಪ್ರಶ್ನೆ ಕೇಳಿ ಅಥವಾ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "ta": "இந்த ஆலோசனை பாதுகாப்பானது அல்ல. தயவுசெய்து வேறு கேள்வி கேளுங்கள் அல்லது விவசாய நிபுணரை அணுகவும்.",
            "en": "This advice is not safe. Please ask a different question or consult an agricultural expert.",
        }
    
    def validate_input(self, query: str, language: str) -> ValidationResult:
        """
        Validate user query before LLM processing.
        
        Args:
            query: User query text to validate
            language: Language code (hi, kn, ta, en)
        
        Returns:
            ValidationResult with safety status and blocked keywords
        
        Validates Requirements: 4.1, 4.3, 4.4
        """
        blocked_keywords = self.check_banned_keywords(query)
        
        if blocked_keywords:
            safety_message = self.get_safety_message(language)
            return ValidationResult(
                is_safe=False,
                blocked_keywords=blocked_keywords,
                safety_message=safety_message
            )
        
        return ValidationResult(
            is_safe=True,
            blocked_keywords=[],
            safety_message=None
        )
    
    def validate_output(self, response: str, language: str) -> ValidationResult:
        """
        Validate LLM-generated response before delivery to user.
        
        Args:
            response: LLM-generated response text to validate
            language: Language code (hi, kn, ta, en)
        
        Returns:
            ValidationResult with safety status and blocked keywords
        
        Validates Requirements: 4.2, 4.3, 4.4
        """
        blocked_keywords = self.check_banned_keywords(response)
        
        if blocked_keywords:
            safety_message = self.get_safety_message(language)
            return ValidationResult(
                is_safe=False,
                blocked_keywords=blocked_keywords,
                safety_message=safety_message
            )
        
        return ValidationResult(
            is_safe=True,
            blocked_keywords=[],
            safety_message=None
        )
    
    def check_banned_keywords(self, text: str) -> List[str]:
        """
        Check text for banned keyword patterns.
        
        Args:
            text: Text to check for banned keywords
        
        Returns:
            List of matched banned keyword patterns
        
        Validates Requirements: 4.3, 4.5
        """
        if not text:
            return []
        
        blocked = []
        text_lower = text.lower()
        
        # Check all banned pattern categories
        for category, patterns in self.banned_patterns.items():
            for pattern in patterns:
                # Use case-insensitive matching
                if re.search(pattern, text_lower, re.IGNORECASE):
                    blocked.append(pattern)
        
        return blocked
    
    def get_safety_message(self, language: str) -> str:
        """
        Get localized safety message for the specified language.
        
        Args:
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Localized safety message string
        
        Validates Requirements: 4.4
        """
        # Default to English if language not supported
        return self.safety_messages.get(language, self.safety_messages["en"])
