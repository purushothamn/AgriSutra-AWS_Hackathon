"""
Unit tests for Sentry Agent

Tests the weather and disaster query handling functionality of the Sentry Agent.
"""

import pytest
from datetime import datetime
from agrisutra.agents.sentry_agent import SentryAgent, WeatherData


class TestSentryAgent:
    """Test suite for SentryAgent class"""
    
    @pytest.fixture
    def agent(self):
        """Create a SentryAgent instance for testing"""
        return SentryAgent()
    
    def test_initialization(self, agent):
        """Test that SentryAgent initializes correctly"""
        assert agent is not None
        assert hasattr(agent, 'mock_weather_data')
        assert hasattr(agent, 'mitigation_steps')
        assert len(agent.mock_weather_data) > 0
    
    def test_fetch_weather_data_valid_location(self, agent):
        """Test fetching weather data for a valid location"""
        weather = agent.fetch_weather_data("bangalore")
        assert weather is not None
        assert isinstance(weather, WeatherData)
        assert weather.location == "Bangalore"
        assert weather.source == "mock"
    
    def test_fetch_weather_data_case_insensitive(self, agent):
        """Test that location lookup is case-insensitive"""
        weather1 = agent.fetch_weather_data("BANGALORE")
        weather2 = agent.fetch_weather_data("bangalore")
        weather3 = agent.fetch_weather_data("Bangalore")
        
        assert weather1 is not None
        assert weather2 is not None
        assert weather3 is not None
        assert weather1.location == weather2.location == weather3.location
    
    def test_fetch_weather_data_invalid_location(self, agent):
        """Test fetching weather data for an invalid location"""
        weather = agent.fetch_weather_data("nonexistent_city")
        assert weather is None
    
    def test_detect_disaster_conditions_heavy_rain(self, agent):
        """Test disaster detection for heavy rainfall"""
        weather = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=30.0,
            humidity_percent=70.0,
            rainfall_mm=120.0,  # > 100mm threshold
            wind_speed_kmh=30.0,
            weather_condition="rain",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather) is True
    
    def test_detect_disaster_conditions_high_temperature(self, agent):
        """Test disaster detection for high temperature"""
        weather = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=42.0,  # > 40°C threshold
            humidity_percent=50.0,
            rainfall_mm=0.0,
            wind_speed_kmh=20.0,
            weather_condition="clear",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather) is True
    
    def test_detect_disaster_conditions_strong_wind(self, agent):
        """Test disaster detection for strong winds"""
        weather = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=30.0,
            humidity_percent=60.0,
            rainfall_mm=10.0,
            wind_speed_kmh=55.0,  # > 50 km/h threshold
            weather_condition="storm",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather) is True
    
    def test_detect_disaster_conditions_normal(self, agent):
        """Test disaster detection for normal weather conditions"""
        weather = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=28.0,
            humidity_percent=65.0,
            rainfall_mm=5.0,
            wind_speed_kmh=15.0,
            weather_condition="clear",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather) is False
    
    def test_detect_disaster_conditions_boundary_values(self, agent):
        """Test disaster detection at exact threshold boundaries"""
        # Exactly at threshold - should not trigger
        weather_at_threshold = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=40.0,  # Exactly 40°C
            humidity_percent=60.0,
            rainfall_mm=100.0,  # Exactly 100mm
            wind_speed_kmh=50.0,  # Exactly 50 km/h
            weather_condition="clear",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather_at_threshold) is False
        
        # Just above threshold - should trigger
        weather_above_threshold = WeatherData(
            location="Test",
            timestamp=datetime.now(),
            temperature_celsius=40.1,  # Just above 40°C
            humidity_percent=60.0,
            rainfall_mm=100.0,
            wind_speed_kmh=50.0,
            weather_condition="clear",
            alerts=[],
            source="mock"
        )
        assert agent.detect_disaster_conditions(weather_above_threshold) is True
    
    def test_generate_mitigation_steps_heavy_rain(self, agent):
        """Test mitigation step generation for heavy rain"""
        steps_hi = agent.generate_mitigation_steps("heavy_rain", "hi")
        steps_kn = agent.generate_mitigation_steps("heavy_rain", "kn")
        steps_ta = agent.generate_mitigation_steps("heavy_rain", "ta")
        steps_en = agent.generate_mitigation_steps("heavy_rain", "en")
        
        assert "भारी बारिश" in steps_hi or "बारिश" in steps_hi
        assert "ಭಾರೀ ಮಳೆ" in steps_kn or "ಮಳೆ" in steps_kn
        assert "கனமழை" in steps_ta or "மழை" in steps_ta
        assert "rain" in steps_en.lower()
    
    def test_generate_mitigation_steps_heat_wave(self, agent):
        """Test mitigation step generation for heat wave"""
        steps_hi = agent.generate_mitigation_steps("heat_wave", "hi")
        steps_kn = agent.generate_mitigation_steps("heat_wave", "kn")
        steps_ta = agent.generate_mitigation_steps("heat_wave", "ta")
        steps_en = agent.generate_mitigation_steps("heat_wave", "en")
        
        assert "गर्मी" in steps_hi
        assert "ಬಿಸಿ" in steps_kn
        assert "வெப்ப" in steps_ta
        assert "heat" in steps_en.lower()
    
    def test_generate_mitigation_steps_strong_wind(self, agent):
        """Test mitigation step generation for strong wind"""
        steps_hi = agent.generate_mitigation_steps("strong_wind", "hi")
        steps_kn = agent.generate_mitigation_steps("strong_wind", "kn")
        steps_ta = agent.generate_mitigation_steps("strong_wind", "ta")
        steps_en = agent.generate_mitigation_steps("strong_wind", "en")
        
        assert "हवा" in steps_hi
        assert "ಗಾಳಿ" in steps_kn
        assert "காற்று" in steps_ta
        assert "wind" in steps_en.lower()
    
    def test_generate_mitigation_steps_multiple(self, agent):
        """Test mitigation step generation for multiple disasters"""
        steps_hi = agent.generate_mitigation_steps("multiple", "hi")
        steps_kn = agent.generate_mitigation_steps("multiple", "kn")
        steps_ta = agent.generate_mitigation_steps("multiple", "ta")
        steps_en = agent.generate_mitigation_steps("multiple", "en")
        
        assert "आपदा" in steps_hi
        assert "ವಿಪತ್ತು" in steps_kn
        assert "பேரிடர்" in steps_ta
        assert "disaster" in steps_en.lower()
    
    def test_process_query_normal_weather(self, agent):
        """Test processing a query for normal weather conditions"""
        response = agent.process_query(
            query="What is the weather in Bangalore?",
            location="bangalore",
            language="en"
        )
        
        assert response is not None
        assert "Bangalore" in response
        assert "28.5" in response  # Temperature from mock data
        # Should not contain mitigation advice for normal weather
        assert "advice" not in response.lower() or "सुझाव" not in response
    
    def test_process_query_disaster_weather(self, agent):
        """Test processing a query for disaster weather conditions"""
        response = agent.process_query(
            query="What is the weather in Mumbai?",
            location="mumbai",
            language="en"
        )
        
        assert response is not None
        assert "Mumbai" in response
        assert "120" in response  # Rainfall from mock data
        # Should contain mitigation advice for disaster weather
        assert "advice" in response.lower() or "rain" in response.lower()
    
    def test_process_query_localized_hindi(self, agent):
        """Test processing a query with Hindi language"""
        response = agent.process_query(
            query="दिल्ली का मौसम क्या है?",
            location="delhi",
            language="hi"
        )
        
        assert response is not None
        assert "Delhi" in response or "दिल्ली" in response
        # Should contain Hindi text
        assert any(char in response for char in "तापमान आर्द्रता वर्षा".split())
    
    def test_process_query_localized_kannada(self, agent):
        """Test processing a query with Kannada language"""
        response = agent.process_query(
            query="ಬೆಂಗಳೂರು ಹವಾಮಾನ ಏನು?",
            location="bangalore",
            language="kn"
        )
        
        assert response is not None
        assert "Bangalore" in response or "ಬೆಂಗಳೂರು" in response
        # Should contain Kannada text
        assert any(char in response for char in "ತಾಪಮಾನ ತೇವಾಂಶ ಮಳೆ".split())
    
    def test_process_query_localized_tamil(self, agent):
        """Test processing a query with Tamil language"""
        response = agent.process_query(
            query="சென்னை வானிலை என்ன?",
            location="chennai",
            language="ta"
        )
        
        assert response is not None
        assert "Chennai" in response or "சென்னை" in response
        # Should contain Tamil text
        assert any(char in response for char in "வெப்பநிலை ஈரப்பதம் மழை".split())
    
    def test_process_query_invalid_location(self, agent):
        """Test processing a query for an invalid location"""
        response = agent.process_query(
            query="What is the weather?",
            location="invalid_city",
            language="en"
        )
        
        assert response is not None
        assert "not available" in response.lower() or "sorry" in response.lower()
    
    def test_process_query_multiple_disasters(self, agent):
        """Test processing a query for location with multiple disaster conditions"""
        response = agent.process_query(
            query="What is the weather in Kolkata?",
            location="kolkata",
            language="en"
        )
        
        assert response is not None
        assert "Kolkata" in response
        # Should contain mitigation advice for multiple disasters
        assert "advice" in response.lower() or "disaster" in response.lower()
    
    def test_mock_data_coverage(self, agent):
        """Test that mock data covers various scenarios"""
        # Should have data for multiple cities
        assert len(agent.mock_weather_data) >= 5
        
        # Should have at least one normal weather scenario
        normal_weather = [w for w in agent.mock_weather_data.values() 
                         if not agent.detect_disaster_conditions(w)]
        assert len(normal_weather) > 0
        
        # Should have at least one disaster scenario
        disaster_weather = [w for w in agent.mock_weather_data.values() 
                           if agent.detect_disaster_conditions(w)]
        assert len(disaster_weather) > 0
    
    def test_mitigation_steps_all_languages(self, agent):
        """Test that mitigation steps exist for all supported languages"""
        disaster_types = ["heavy_rain", "heat_wave", "strong_wind", "multiple"]
        languages = ["hi", "kn", "ta", "en"]
        
        for disaster_type in disaster_types:
            for language in languages:
                steps = agent.generate_mitigation_steps(disaster_type, language)
                assert steps is not None
                assert len(steps) > 0
