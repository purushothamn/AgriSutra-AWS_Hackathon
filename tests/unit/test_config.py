"""
Unit tests for configuration module.
"""

import pytest
from agrisutra import config


class TestConfiguration:
    """Test configuration settings and helper functions."""

    def test_supported_languages(self):
        """Test that all supported languages are defined."""
        assert len(config.SUPPORTED_LANGUAGES) == 3
        assert "hi" in config.SUPPORTED_LANGUAGES
        assert "kn" in config.SUPPORTED_LANGUAGES
        assert "ta" in config.SUPPORTED_LANGUAGES

    def test_language_code_mapping(self):
        """Test language code mapping for AWS services."""
        assert config.get_language_code("hi") == "hi-IN"
        assert config.get_language_code("kn") == "kn-IN"
        assert config.get_language_code("ta") == "ta-IN"
        # Test default fallback
        assert config.get_language_code("unknown") == "hi-IN"

    def test_voice_id_mapping(self):
        """Test voice ID mapping for AWS Polly."""
        assert config.get_voice_id("hi") == "Aditi"
        assert config.get_voice_id("kn") == "Kajal"
        assert config.get_voice_id("ta") == "Aria"
        # Test default fallback
        assert config.get_voice_id("unknown") == "Aditi"

    def test_system_prompt_generation(self):
        """Test system prompt template generation."""
        prompt_hi = config.get_system_prompt("hi")
        assert "AgriSutra" in prompt_hi
        assert "hi" in prompt_hi
        assert "3-5 sentences" in prompt_hi
        
        prompt_kn = config.get_system_prompt("kn")
        assert "kn" in prompt_kn

    def test_bedrock_model_params(self):
        """Test Bedrock model parameters are correctly set."""
        assert config.BEDROCK_MODEL_PARAMS["max_tokens"] == 500
        assert config.BEDROCK_MODEL_PARAMS["temperature"] == 0.7
        assert config.BEDROCK_MODEL_PARAMS["top_p"] == 0.9

    def test_bedrock_model_id(self):
        """Test Bedrock model ID is Claude 3 Haiku."""
        assert "claude-3-haiku" in config.BEDROCK_MODEL_ID
        assert "anthropic" in config.BEDROCK_MODEL_ID

    def test_transcribe_config(self):
        """Test AWS Transcribe configuration."""
        assert config.TRANSCRIBE_CONFIG["MediaFormat"] == "wav"
        assert config.TRANSCRIBE_CONFIG["MediaSampleRateHertz"] == 16000

    def test_polly_config(self):
        """Test AWS Polly configuration."""
        assert config.POLLY_CONFIG["Engine"] == "neural"
        assert config.POLLY_CONFIG["OutputFormat"] == "mp3"

    def test_cache_configuration(self):
        """Test cache TTL settings."""
        assert config.WEATHER_CACHE_TTL_MINUTES == 15
        assert config.TRANSLATION_CACHE_PERMANENT is True
        assert config.DYNAMODB_TTL_HOURS == 24

    def test_performance_targets(self):
        """Test performance target settings."""
        assert config.COLD_START_TARGET_SECONDS == 15
        assert config.WARM_START_TARGET_SECONDS == 8

    def test_s3_bucket_structure(self):
        """Test S3 bucket structure paths."""
        assert "weather/" in config.S3_BUCKET_STRUCTURE["weather"]
        assert "translations/images/" in config.S3_BUCKET_STRUCTURE["translations_images"]
        assert "translations/audio/" in config.S3_BUCKET_STRUCTURE["translations_audio"]
        assert "responses/" in config.S3_BUCKET_STRUCTURE["responses"]
