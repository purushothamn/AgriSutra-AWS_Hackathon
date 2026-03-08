"""
AgriSutra - Voice-First Farm Intelligence System

A vernacular, voice-first farm intelligence system for rural farmers in India.
Supports Hindi, Kannada, and Tamil languages with specialized agents for weather
alerts and crop economics, governed by safety rules.
"""

__version__ = "0.1.0"

from agrisutra.orchestrator import LambdaOrchestrator, OrchestratorResponse
from agrisutra.groq_client import GroqClient
from agrisutra.speech_client import SpeechClient
from agrisutra.voice_pipeline import VoicePipeline
from agrisutra.safety import ResilienceSentry, ValidationResult
from agrisutra.agents import (
    IntentRouter,
    Intent,
    SentryAgent,
    WeatherData,
    EconomistAgent,
    ROIEstimate,
    MarketData
)
from agrisutra.translation import ContextTranslator, TechnicalTerm, TranslatedResponse

__all__ = [
    "LambdaOrchestrator",
    "OrchestratorResponse",
    "GroqClient",
    "SpeechClient",
    "VoicePipeline",
    "ResilienceSentry",
    "ValidationResult",
    "IntentRouter",
    "Intent",
    "SentryAgent",
    "WeatherData",
    "EconomistAgent",
    "ROIEstimate",
    "MarketData",
    "ContextTranslator",
    "TechnicalTerm",
    "TranslatedResponse",
]
