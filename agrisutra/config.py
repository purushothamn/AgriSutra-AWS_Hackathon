"""
Configuration file for AWS service endpoints and model IDs.
"""

import os
from typing import Dict

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# AWS Bedrock Configuration
BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
BEDROCK_MODEL_PARAMS = {
    "max_tokens": 500,  # Increased for more detailed responses
    "temperature": 0.7,
    "top_p": 0.9
}

# AWS Transcribe Configuration
TRANSCRIBE_CONFIG = {
    "MediaFormat": "wav",
    "MediaSampleRateHertz": 16000
}

# Language code mapping for AWS services
LANGUAGE_CODES = {
    "hi": "hi-IN",  # Hindi
    "kn": "kn-IN",  # Kannada
    "ta": "ta-IN"   # Tamil
}

# AWS Polly Configuration
POLLY_CONFIG = {
    "Engine": "neural",
    "OutputFormat": "mp3"
}

# Voice ID mapping for AWS Polly
POLLY_VOICE_IDS = {
    "hi": "Aditi",   # Hindi
    "kn": "Kajal",   # Kannada
    "ta": "Aria"     # Tamil (using closest available)
}

# AWS S3 Configuration
S3_CACHE_BUCKET = os.getenv("S3_CACHE_BUCKET", "agrisutra-cache")
S3_BUCKET_STRUCTURE = {
    "weather": "weather/",
    "translations_images": "translations/images/",
    "translations_audio": "translations/audio/",
    "responses": "responses/"
}

# AWS DynamoDB Configuration
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "agrisutra-sessions")
DYNAMODB_TTL_HOURS = 24

# External API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cache Configuration
WEATHER_CACHE_TTL_MINUTES = 15
TRANSLATION_CACHE_PERMANENT = True

# Performance Targets
COLD_START_TARGET_SECONDS = 15
WARM_START_TARGET_SECONDS = 8

# System Prompt Template
SYSTEM_PROMPT_TEMPLATE = """You are AgriSutra, an expert AI farming assistant for Indian farmers.
Language: {language}

Your role:
- Provide practical, actionable farming advice
- Answer questions about crops, weather, soil, irrigation, pests, fertilizers, and farm management
- Give specific recommendations based on Indian farming conditions
- Use simple, clear language that farmers can understand
- Include numbers, measurements, and timelines when relevant

Rules:
1. Keep responses concise (3-5 sentences for simple questions, more for complex topics)
2. Provide step-by-step guidance when explaining processes
3. Focus on practical, implementable advice
4. Consider local Indian farming practices and conditions
5. Mention safety precautions when discussing chemicals or equipment
6. If weather or crop finance data is provided in the query, use it in your response
7. ALWAYS answer the specific question asked - do not give generic greetings
8. For weather queries, provide current conditions and farming implications

Always prioritize farmer safety and sustainable farming practices.
"""

# Supported Languages
SUPPORTED_LANGUAGES = ["hi", "kn", "ta"]

def get_language_code(language: str) -> str:
    """Get AWS language code for a given language."""
    return LANGUAGE_CODES.get(language, "hi-IN")

def get_voice_id(language: str) -> str:
    """Get AWS Polly voice ID for a given language."""
    return POLLY_VOICE_IDS.get(language, "Aditi")

def get_system_prompt(language: str) -> str:
    """Get system prompt for a given language."""
    return SYSTEM_PROMPT_TEMPLATE.format(language=language)
