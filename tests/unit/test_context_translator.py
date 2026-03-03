"""Unit tests for ContextTranslator."""

import pytest
from agrisutra.translation import ContextTranslator, TechnicalTerm, TranslatedResponse


class TestContextTranslator:
    """Test suite for ContextTranslator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.translator = ContextTranslator()
    
    def test_initialization(self):
        """Test ContextTranslator initialization."""
        assert self.translator is not None
        assert len(ContextTranslator.TRANSLATION_DICT) >= 10
    
    def test_translate_technical_terms_hindi(self):
        """Test translation of technical terms to Hindi."""
        text = "Use drip irrigation for better water management."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert isinstance(result, TranslatedResponse)
        assert result.original_text == text
        assert "बूंद-बूंद सिंचाई" in result.translated_text
        assert len(result.technical_terms) == 1
        assert result.technical_terms[0].original == "drip irrigation"
        assert result.technical_terms[0].translation == "बूंद-बूंद सिंचाई"
    
    def test_translate_technical_terms_kannada(self):
        """Test translation of technical terms to Kannada."""
        text = "Apply NPK fertilizer to improve crop yield."
        result = self.translator.translate_technical_terms(text, "kn")
        
        assert isinstance(result, TranslatedResponse)
        assert "ಎನ್‌ಪಿಕೆ ಗೊಬ್ಬರ" in result.translated_text
        assert len(result.technical_terms) == 1
        assert result.technical_terms[0].translation == "ಎನ್‌ಪಿಕೆ ಗೊಬ್ಬರ"
    
    def test_translate_technical_terms_tamil(self):
        """Test translation of technical terms to Tamil."""
        text = "Use pesticide carefully to protect crops."
        result = self.translator.translate_technical_terms(text, "ta")
        
        assert isinstance(result, TranslatedResponse)
        assert "பூச்சிக்கொல்லி" in result.translated_text
        assert len(result.technical_terms) == 1
        assert result.technical_terms[0].translation == "பூச்சிக்கொல்லி"
    
    def test_translate_multiple_terms(self):
        """Test translation of multiple technical terms in one text."""
        text = "Use drip irrigation and NPK fertilizer for organic farming."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert len(result.technical_terms) == 3
        term_originals = [t.original for t in result.technical_terms]
        assert "drip irrigation" in term_originals
        assert "NPK fertilizer" in term_originals
        assert "organic farming" in term_originals
    
    def test_translate_case_insensitive(self):
        """Test that translation works with different cases."""
        text = "Use Drip Irrigation for better results."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert len(result.technical_terms) == 1
        assert result.technical_terms[0].original == "Drip Irrigation"
    
    def test_translate_no_technical_terms(self):
        """Test translation when no technical terms are present."""
        text = "This is a simple sentence without technical terms."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert result.original_text == text
        assert result.translated_text == text
        assert len(result.technical_terms) == 0
    
    def test_translate_unsupported_language(self):
        """Test that unsupported language raises ValueError."""
        text = "Use drip irrigation."
        
        with pytest.raises(ValueError, match="Unsupported language"):
            self.translator.translate_technical_terms(text, "en")
    
    def test_get_term_image(self):
        """Test image URL generation for technical terms."""
        url = self.translator.get_term_image("drip irrigation")
        
        assert url.startswith("https://agrisutra-assets.s3.ap-south-1.amazonaws.com")
        assert "translations/images/drip_irrigation.jpg" in url
    
    def test_get_term_image_normalization(self):
        """Test that term names are normalized in image URLs."""
        url = self.translator.get_term_image("NPK Fertilizer")
        
        assert "npk_fertilizer.jpg" in url
        assert " " not in url
    
    def test_get_term_audio_hindi(self):
        """Test audio URL generation for Hindi."""
        url = self.translator.get_term_audio("drip irrigation", "hi")
        
        assert url.startswith("https://agrisutra-assets.s3.ap-south-1.amazonaws.com")
        assert "translations/audio/drip_irrigation_hi.mp3" in url
    
    def test_get_term_audio_kannada(self):
        """Test audio URL generation for Kannada."""
        url = self.translator.get_term_audio("pesticide", "kn")
        
        assert "translations/audio/pesticide_kn.mp3" in url
    
    def test_get_term_audio_tamil(self):
        """Test audio URL generation for Tamil."""
        url = self.translator.get_term_audio("greenhouse", "ta")
        
        assert "translations/audio/greenhouse_ta.mp3" in url
    
    def test_get_term_audio_unsupported_language(self):
        """Test that unsupported language raises ValueError for audio."""
        with pytest.raises(ValueError, match="Unsupported language"):
            self.translator.get_term_audio("drip irrigation", "fr")
    
    def test_technical_term_has_image_and_audio(self):
        """Test that translated technical terms include image and audio URLs."""
        text = "Use drip irrigation."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert len(result.technical_terms) == 1
        term = result.technical_terms[0]
        assert term.image_url != ""
        assert term.audio_url != ""
        assert "drip_irrigation" in term.image_url
        assert "drip_irrigation_hi" in term.audio_url
    
    def test_technical_term_has_local_analogy(self):
        """Test that translated terms include local language analogies."""
        text = "Use drip irrigation."
        result = self.translator.translate_technical_terms(text, "hi")
        
        assert len(result.technical_terms) == 1
        term = result.technical_terms[0]
        assert term.local_analogy != ""
        assert "पानी की बूंदों से सिंचाई" in term.local_analogy
    
    def test_translation_dictionary_completeness(self):
        """Test that translation dictionary has entries for all supported languages."""
        for term, translations in ContextTranslator.TRANSLATION_DICT.items():
            assert "hi" in translations, f"Hindi translation missing for {term}"
            assert "kn" in translations, f"Kannada translation missing for {term}"
            assert "ta" in translations, f"Tamil translation missing for {term}"
            
            for lang in ["hi", "kn", "ta"]:
                assert "translation" in translations[lang]
                assert "analogy" in translations[lang]
    
    def test_translation_dictionary_size(self):
        """Test that translation dictionary has at least 10-15 terms."""
        assert len(ContextTranslator.TRANSLATION_DICT) >= 10
        assert len(ContextTranslator.TRANSLATION_DICT) <= 20
