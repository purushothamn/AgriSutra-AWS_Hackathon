"""
Lambda Orchestrator - Request Flow Coordinator

This module implements the main orchestrator that coordinates the request flow
between all AgriSutra components: Voice Pipeline, Resilience Sentry, Intent Router,
Agents, LLM Client, and Context Translator.

Validates Requirements: 2.3, 2.4, 2.5, 3.6, 4.1, 4.2, 5.1
"""

import time
from typing import Dict, Optional, Any
from dataclasses import dataclass
from agrisutra.voice_pipeline import VoicePipeline
from agrisutra.safety import ResilienceSentry
from agrisutra.agents import IntentRouter, SentryAgent, EconomistAgent, Intent
from agrisutra.translation import ContextTranslator
from agrisutra.groq_client import GroqClient
from agrisutra.speech_recognition import GroqSpeechRecognition


@dataclass
class OrchestratorResponse:
    """Response from the orchestrator"""
    success: bool
    text_response: str
    audio_response: Optional[bytes]
    technical_terms: list
    error_message: Optional[str]
    processing_time_ms: int


class LambdaOrchestrator:
    """
    Main orchestrator that coordinates request flow through all AgriSutra components.
    
    Handles the complete pipeline: voice input → safety check → intent routing →
    agent processing → LLM generation → safety validation → translation → voice output.
    """
    
    def __init__(self, groq_api_key: str):
        """
        Initialize the orchestrator with all required components
        
        Args:
            groq_api_key: Groq API key for LLM (required)
        """
        self.voice_pipeline = VoicePipeline(groq_api_key=groq_api_key, use_mock=False)
        self.resilience_sentry = ResilienceSentry()
        self.intent_router = IntentRouter()
        self.sentry_agent = SentryAgent()
        self.economist_agent = EconomistAgent()
        self.context_translator = ContextTranslator()
        self.llm_client = GroqClient(api_key=groq_api_key)
        self.speech_recognition = GroqSpeechRecognition(api_key=groq_api_key)
        
        # Simple in-memory cache for MVP
        self.cache = {}
    
    def handle_request(self, event: Dict) -> OrchestratorResponse:
        """
        Main entry point for handling requests.
        
        Args:
            event: Request event dictionary containing:
                - input_type: "audio" or "text"
                - input_data: audio bytes or text string
                - language: language code (hi, kn, ta, en)
                - location: optional location for weather queries
                - crop: optional crop name for finance queries
                - area: optional farm area for finance queries
        
        Returns:
            OrchestratorResponse with processed result
        
        Validates Requirements: 2.3, 2.4, 2.5, 3.6, 4.1, 4.2
        """
        start_time = time.time()
        
        try:
            # Extract request parameters
            input_type = event.get("input_type", "text")
            input_data = event.get("input_data")
            language = event.get("language", "en")
            location = event.get("location", "bangalore")
            crop = event.get("crop", "rice")
            area = event.get("area", 1.0)
            
            # Step 1: Process input (transcribe if audio)
            if input_type == "audio":
                query_text = self.speech_recognition.transcribe(input_data, language)
                if query_text is None:
                    return self._create_error_response(
                        "Failed to transcribe audio. Please try again or use text input.",
                        language,
                        start_time
                    )
            else:
                query_text = input_data
            
            if not query_text:
                return self._create_error_response(
                    "Empty query received.",
                    language,
                    start_time
                )
            
            # Step 2: Safety check on input
            input_validation = self.resilience_sentry.validate_input(query_text, language)
            if not input_validation.is_safe:
                # Return safety message without processing
                audio_response = self.voice_pipeline.synthesize_speech(
                    input_validation.safety_message,
                    language
                )
                
                processing_time = int((time.time() - start_time) * 1000)
                return OrchestratorResponse(
                    success=False,
                    text_response=input_validation.safety_message,
                    audio_response=audio_response,
                    technical_terms=[],
                    error_message="Safety violation detected",
                    processing_time_ms=processing_time
                )
            
            # Step 3: Classify intent and route to agent
            intent = self.intent_router.classify_intent(query_text, language)
            agent_name = self.intent_router.route_to_agent(query_text, intent)
            
            # Step 4: Get context from specialized agents if applicable
            agent_context = ""
            if agent_name == "sentry":
                # Get weather data to provide as context to LLM
                weather_data = self.sentry_agent.fetch_weather_data(location)
                if weather_data:
                    agent_context = f"\n\nWeather Context for {location}: Temperature {weather_data.temperature_celsius}°C, Humidity {weather_data.humidity_percent}%, Rainfall {weather_data.rainfall_mm}mm, Wind {weather_data.wind_speed_kmh} km/h."
                    if self.sentry_agent.detect_disaster_conditions(weather_data):
                        agent_context += " WARNING: Disaster conditions detected!"
            
            elif agent_name == "economist":
                # Get crop data to provide as context to LLM
                roi = self.economist_agent.calculate_roi(crop, area)
                if roi:
                    agent_context = f"\n\nCrop Finance Context for {crop} ({area} acres): Total cost ₹{roi.total_cost:,.0f}, Expected yield {roi.expected_yield:,.0f} kg, Expected revenue ₹{roi.expected_revenue:,.0f}, ROI {roi.roi_percentage:.1f}%, Breakeven price ₹{roi.breakeven_price:.2f}/kg."
            
            # Step 5: Generate response using LLM with context
            enriched_query = query_text + agent_context
            agent_response = self.llm_client.generate_response(enriched_query, language)
            
            if agent_response is None:
                return self._create_error_response(
                    "Failed to generate response. Please try again.",
                    language,
                    start_time
                )
            
            # Step 5: Safety check on output
            output_validation = self.resilience_sentry.validate_output(agent_response, language)
            if not output_validation.is_safe:
                # Return safety message instead of unsafe response
                audio_response = self.voice_pipeline.synthesize_speech(
                    output_validation.safety_message,
                    language
                )
                
                processing_time = int((time.time() - start_time) * 1000)
                return OrchestratorResponse(
                    success=False,
                    text_response=output_validation.safety_message,
                    audio_response=audio_response,
                    technical_terms=[],
                    error_message="Unsafe response blocked",
                    processing_time_ms=processing_time
                )
            
            # Step 6: Translate technical terms (if language is not English)
            if language in ["hi", "kn", "ta"]:
                translated_response = self.context_translator.translate_technical_terms(
                    agent_response,
                    language
                )
                final_text = translated_response.translated_text
                technical_terms = translated_response.technical_terms
            else:
                final_text = agent_response
                technical_terms = []
            
            # Step 7: Synthesize speech
            audio_response = self.voice_pipeline.synthesize_speech(final_text, language)
            
            # Calculate processing time
            processing_time = int((time.time() - start_time) * 1000)
            
            return OrchestratorResponse(
                success=True,
                text_response=final_text,
                audio_response=audio_response,
                technical_terms=technical_terms,
                error_message=None,
                processing_time_ms=processing_time
            )
        
        except Exception as e:
            return self._create_error_response(
                f"An error occurred: {str(e)}",
                event.get("language", "en"),
                start_time
            )
    
    def _create_error_response(
        self,
        error_message: str,
        language: str,
        start_time: float
    ) -> OrchestratorResponse:
        """
        Create an error response with localized message.
        
        Args:
            error_message: Error message in English
            language: Language code for localization
            start_time: Request start time for calculating processing time
        
        Returns:
            OrchestratorResponse with error details
        """
        # Localize error message
        error_messages = {
            "hi": "क्षमा करें, एक त्रुटि हुई। कृपया फिर से प्रयास करें।",
            "kn": "ಕ್ಷಮಿಸಿ, ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
            "ta": "மன்னிக்கவும், பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
            "en": "Sorry, an error occurred. Please try again."
        }
        
        localized_message = error_messages.get(language, error_messages["en"])
        
        # Try to synthesize error message
        audio_response = self.voice_pipeline.synthesize_speech(localized_message, language)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return OrchestratorResponse(
            success=False,
            text_response=localized_message,
            audio_response=audio_response,
            technical_terms=[],
            error_message=error_message,
            processing_time_ms=processing_time
        )
    
    def get_cached_response(self, cache_key: str) -> Optional[Dict]:
        """
        Retrieve cached response.
        
        Args:
            cache_key: Cache key string
        
        Returns:
            Cached response dictionary or None if not found
        """
        return self.cache.get(cache_key)
    
    def set_cached_response(self, cache_key: str, response: Dict, ttl_seconds: int = 900):
        """
        Store response in cache.
        
        Args:
            cache_key: Cache key string
            response: Response dictionary to cache
            ttl_seconds: Time-to-live in seconds (default: 15 minutes)
        """
        self.cache[cache_key] = {
            "response": response,
            "expires_at": time.time() + ttl_seconds
        }
    
    def clear_expired_cache(self):
        """Remove expired entries from cache"""
        current_time = time.time()
        
        expired_keys = [
            key for key, value in self.cache.items()
            if value.get("expires_at", 0) < current_time
        ]
        
        for key in expired_keys:
            del self.cache[key]
