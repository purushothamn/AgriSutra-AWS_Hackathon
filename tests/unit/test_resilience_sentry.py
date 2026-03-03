"""
Unit tests for ResilienceSentry class

Tests banned keyword detection, safety message localization, and edge cases.
Validates Requirements: 4.1, 4.2, 4.3, 4.4
"""

import pytest
from agrisutra.safety import ResilienceSentry, ValidationResult


class TestResilienceSentry:
    """Test suite for ResilienceSentry safety governance layer"""
    
    @pytest.fixture
    def sentry(self):
        """Create a ResilienceSentry instance for testing"""
        return ResilienceSentry()
    
    # Test banned keyword detection for chemical mixing
    
    def test_detect_chemical_mixing_english(self, sentry):
        """Test detection of chemical mixing keywords in English"""
        query = "Can I mix pesticide with water?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
        assert result.safety_message is not None
    
    def test_detect_chemical_mixing_hindi(self, sentry):
        """Test detection of chemical mixing keywords in Hindi"""
        query = "क्या मैं कीटनाशक मिला सकता हूं?"
        result = sentry.validate_input(query, "hi")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
        assert result.safety_message is not None
        assert "सुरक्षित नहीं" in result.safety_message
    
    def test_detect_chemical_mixing_kannada(self, sentry):
        """Test detection of chemical mixing keywords in Kannada"""
        query = "ಕೀಟನಾಶಕ ಮಿಶ್ರಣ ಮಾಡಬಹುದೇ?"
        result = sentry.validate_input(query, "kn")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
        assert result.safety_message is not None
        assert "ಸುರಕ್ಷಿತವಲ್ಲ" in result.safety_message
    
    def test_detect_chemical_mixing_tamil(self, sentry):
        """Test detection of chemical mixing keywords in Tamil"""
        query = "பூச்சிக்கொல்லி கலக்கலாமா?"
        result = sentry.validate_input(query, "ta")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
        assert result.safety_message is not None
        assert "பாதுகாப்பானது அல்ல" in result.safety_message
    
    # Test banned keyword detection for unsafe practices
    
    def test_detect_unsafe_practice_english(self, sentry):
        """Test detection of unsafe practice keywords in English"""
        query = "Should I burn crop stubble?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    def test_detect_unsafe_practice_hindi(self, sentry):
        """Test detection of unsafe practice keywords in Hindi"""
        query = "क्या मुझे फसल जलाना चाहिए?"
        result = sentry.validate_input(query, "hi")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    def test_detect_unsafe_practice_kannada(self, sentry):
        """Test detection of unsafe practice keywords in Kannada"""
        query = "ಬೆಳೆ ಸುಡುವುದು ಸರಿಯೇ?"
        result = sentry.validate_input(query, "kn")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    # Test banned keyword detection for ignoring warnings
    
    def test_detect_ignore_warning_english(self, sentry):
        """Test detection of ignore warning keywords in English"""
        query = "Can I ignore warning labels?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    def test_detect_ignore_warning_hindi(self, sentry):
        """Test detection of ignore warning keywords in Hindi"""
        query = "क्या मैं चेतावनी अनदेखा कर सकता हूं?"
        result = sentry.validate_input(query, "hi")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    # Test safe queries (should pass validation)
    
    def test_safe_query_english(self, sentry):
        """Test that safe queries pass validation"""
        query = "What is the best fertilizer for wheat?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
        assert result.safety_message is None
    
    def test_safe_query_hindi(self, sentry):
        """Test that safe queries in Hindi pass validation"""
        query = "गेहूं के लिए सबसे अच्छा उर्वरक क्या है?"
        result = sentry.validate_input(query, "hi")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
        assert result.safety_message is None
    
    def test_safe_query_kannada(self, sentry):
        """Test that safe queries in Kannada pass validation"""
        query = "ಗೋಧಿಗೆ ಉತ್ತಮ ಗೊಬ್ಬರ ಯಾವುದು?"
        result = sentry.validate_input(query, "kn")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
        assert result.safety_message is None
    
    # Test output validation
    
    def test_validate_output_with_banned_keyword(self, sentry):
        """Test that output validation detects banned keywords"""
        response = "You should mix pesticide with fertilizer for better results."
        result = sentry.validate_output(response, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
        assert result.safety_message is not None
    
    def test_validate_output_safe(self, sentry):
        """Test that safe output passes validation"""
        response = "Use organic fertilizer for better soil health."
        result = sentry.validate_output(response, "en")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
        assert result.safety_message is None
    
    # Test localized safety messages
    
    def test_safety_message_hindi(self, sentry):
        """Test Hindi safety message generation"""
        message = sentry.get_safety_message("hi")
        assert "सुरक्षित नहीं" in message
        assert "कृपया" in message
    
    def test_safety_message_kannada(self, sentry):
        """Test Kannada safety message generation"""
        message = sentry.get_safety_message("kn")
        assert "ಸುರಕ್ಷಿತವಲ್ಲ" in message
        assert "ದಯವಿಟ್ಟು" in message
    
    def test_safety_message_tamil(self, sentry):
        """Test Tamil safety message generation"""
        message = sentry.get_safety_message("ta")
        assert "பாதுகாப்பானது அல்ல" in message
        assert "தயவுசெய்து" in message
    
    def test_safety_message_english(self, sentry):
        """Test English safety message generation"""
        message = sentry.get_safety_message("en")
        assert "not safe" in message.lower()
        assert "please" in message.lower()
    
    def test_safety_message_unsupported_language(self, sentry):
        """Test that unsupported language defaults to English"""
        message = sentry.get_safety_message("fr")
        assert "not safe" in message.lower()
    
    # Test edge cases
    
    def test_empty_query(self, sentry):
        """Test validation of empty query"""
        result = sentry.validate_input("", "en")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
    
    def test_none_query(self, sentry):
        """Test validation of None query"""
        result = sentry.validate_input(None, "en")
        
        assert result.is_safe is True
        assert len(result.blocked_keywords) == 0
    
    def test_case_insensitive_matching(self, sentry):
        """Test that keyword matching is case-insensitive"""
        query = "Can I MIX PESTICIDE with water?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    def test_partial_match_with_spacing(self, sentry):
        """Test that patterns match with various spacing"""
        query = "Can I mix   pesticide with water?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) > 0
    
    def test_multiple_banned_keywords(self, sentry):
        """Test detection of multiple banned keywords in one query"""
        query = "Can I mix pesticide and burn crop stubble?"
        result = sentry.validate_input(query, "en")
        
        assert result.is_safe is False
        assert len(result.blocked_keywords) >= 2
