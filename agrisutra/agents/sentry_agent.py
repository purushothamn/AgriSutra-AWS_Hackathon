"""
Sentry Agent - Weather and Disaster Query Handler

This module implements the Sentry Agent that handles weather and disaster-related queries.
For the MVP, it uses hardcoded mock weather data instead of calling external APIs.

Validates Requirements: 3.1, 3.3, 3.4
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    """Weather data model for a specific location"""
    location: str
    timestamp: datetime
    temperature_celsius: float
    humidity_percent: float
    rainfall_mm: float
    wind_speed_kmh: float
    weather_condition: str  # "clear" | "rain" | "storm"
    alerts: List[str]
    source: str  # "api" | "cache" | "mock"


class SentryAgent:
    """
    Sentry Agent handles weather and disaster-related queries.
    
    For the MVP, this agent uses hardcoded mock weather data for demonstration purposes.
    It detects disaster conditions based on thresholds and provides localized mitigation advice.
    """
    
    def __init__(self):
        """Initialize the Sentry Agent with mock weather data"""
        self._initialize_mock_data()
        self._initialize_mitigation_steps()
    
    def _initialize_mock_data(self):
        """Initialize hardcoded mock weather data for demo locations"""
        self.mock_weather_data = {
            # Normal weather conditions
            "bangalore": WeatherData(
                location="Bangalore",
                timestamp=datetime.now(),
                temperature_celsius=28.5,
                humidity_percent=65.0,
                rainfall_mm=5.0,
                wind_speed_kmh=15.0,
                weather_condition="clear",
                alerts=[],
                source="mock"
            ),
            "bengaluru": WeatherData(  # Alternate spelling
                location="Bengaluru",
                timestamp=datetime.now(),
                temperature_celsius=28.5,
                humidity_percent=65.0,
                rainfall_mm=5.0,
                wind_speed_kmh=15.0,
                weather_condition="clear",
                alerts=[],
                source="mock"
            ),
            # Heavy rainfall scenario
            "mumbai": WeatherData(
                location="Mumbai",
                timestamp=datetime.now(),
                temperature_celsius=32.0,
                humidity_percent=85.0,
                rainfall_mm=120.0,  # Heavy rainfall > 100mm
                wind_speed_kmh=45.0,
                weather_condition="rain",
                alerts=["Heavy rainfall warning"],
                source="mock"
            ),
            # High temperature scenario
            "delhi": WeatherData(
                location="Delhi",
                timestamp=datetime.now(),
                temperature_celsius=42.0,  # High temperature > 40°C
                humidity_percent=40.0,
                rainfall_mm=0.0,
                wind_speed_kmh=20.0,
                weather_condition="clear",
                alerts=["Heat wave warning"],
                source="mock"
            ),
            # Strong winds scenario
            "chennai": WeatherData(
                location="Chennai",
                timestamp=datetime.now(),
                temperature_celsius=35.0,
                humidity_percent=75.0,
                rainfall_mm=15.0,
                wind_speed_kmh=55.0,  # Strong winds > 50 km/h
                weather_condition="storm",
                alerts=["Strong wind warning"],
                source="mock"
            ),
            # Multiple disaster conditions
            "kolkata": WeatherData(
                location="Kolkata",
                timestamp=datetime.now(),
                temperature_celsius=38.0,
                humidity_percent=90.0,
                rainfall_mm=110.0,  # Heavy rainfall
                wind_speed_kmh=60.0,  # Strong winds
                weather_condition="storm",
                alerts=["Heavy rainfall warning", "Strong wind warning"],
                source="mock"
            ),
            # Normal conditions - another example
            "pune": WeatherData(
                location="Pune",
                timestamp=datetime.now(),
                temperature_celsius=30.0,
                humidity_percent=60.0,
                rainfall_mm=2.0,
                wind_speed_kmh=12.0,
                weather_condition="clear",
                alerts=[],
                source="mock"
            ),
        }
    
    def _initialize_mitigation_steps(self):
        """Initialize localized mitigation advice for different disaster types"""
        self.mitigation_steps = {
            "heavy_rain": {
                "hi": "भारी बारिश के लिए सुझाव: 1) खेत में जल निकासी की व्यवस्था करें 2) फसल को सहारा दें 3) कीटनाशक का छिड़काव टालें",
                "kn": "ಭಾರೀ ಮಳೆಗೆ ಸಲಹೆ: 1) ಹೊಲದಲ್ಲಿ ನೀರು ಹರಿಯುವ ವ್ಯವಸ್ಥೆ ಮಾಡಿ 2) ಬೆಳೆಗೆ ಬೆಂಬಲ ನೀಡಿ 3) ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸುವುದನ್ನು ತಪ್ಪಿಸಿ",
                "ta": "கனமழைக்கான ஆலோசனை: 1) வயலில் வடிகால் ஏற்பாடு செய்யுங்கள் 2) பயிருக்கு ஆதரவு கொடுங்கள் 3) பூச்சிக்கொல்லி தெளிப்பதை தவிர்க்கவும்",
                "en": "Heavy rain advice: 1) Ensure proper drainage in field 2) Provide support to crops 3) Avoid pesticide spraying"
            },
            "heat_wave": {
                "hi": "गर्मी की लहर के लिए सुझाव: 1) सुबह या शाम को सिंचाई करें 2) मल्चिंग का उपयोग करें 3) छाया जाल लगाएं",
                "kn": "ಬಿಸಿ ಅಲೆಗೆ ಸಲಹೆ: 1) ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಸಂಜೆ ನೀರಾವರಿ ಮಾಡಿ 2) ಮಲ್ಚಿಂಗ್ ಬಳಸಿ 3) ನೆರಳು ಬಲೆ ಹಾಕಿ",
                "ta": "வெப்ப அலைக்கான ஆலோசனை: 1) காலை அல்லது மாலை நீர்ப்பாசனம் செய்யுங்கள் 2) மல்ச்சிங் பயன்படுத்துங்கள் 3) நிழல் வலை அமைக்கவும்",
                "en": "Heat wave advice: 1) Irrigate in morning or evening 2) Use mulching 3) Install shade nets"
            },
            "strong_wind": {
                "hi": "तेज हवा के लिए सुझाव: 1) फसल को खूंटे से बांधें 2) ढीली वस्तुओं को सुरक्षित करें 3) पॉलीहाउस की जांच करें",
                "kn": "ಬಲವಾದ ಗಾಳಿಗೆ ಸಲಹೆ: 1) ಬೆಳೆಯನ್ನು ಕಂಬಗಳಿಗೆ ಕಟ್ಟಿ 2) ಸಡಿಲವಾದ ವಸ್ತುಗಳನ್ನು ಸುರಕ್ಷಿತಗೊಳಿಸಿ 3) ಪಾಲಿಹೌಸ್ ಪರಿಶೀಲಿಸಿ",
                "ta": "வலுவான காற்றுக்கான ஆலோசனை: 1) பயிரை கம்புகளில் கட்டுங்கள் 2) தளர்வான பொருட்களை பாதுகாக்கவும் 3) பாலிஹவுஸை சரிபார்க்கவும்",
                "en": "Strong wind advice: 1) Tie crops to stakes 2) Secure loose items 3) Check polyhouse"
            },
            "multiple": {
                "hi": "कई आपदाओं के लिए सुझाव: 1) तत्काल सुरक्षा उपाय करें 2) स्थानीय अधिकारियों से संपर्क करें 3) फसल बीमा की जांच करें",
                "kn": "ಅನೇಕ ವಿಪತ್ತುಗಳಿಗೆ ಸಲಹೆ: 1) ತಕ್ಷಣ ಸುರಕ್ಷತಾ ಕ್ರಮಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ 2) ಸ್ಥಳೀಯ ಅಧಿಕಾರಿಗಳನ್ನು ಸಂಪರ್ಕಿಸಿ 3) ಬೆಳೆ ವಿಮೆ ಪರಿಶೀಲಿಸಿ",
                "ta": "பல பேரிடர்களுக்கான ஆலோசனை: 1) உடனடி பாதுகாப்பு நடவடிக்கைகள் எடுங்கள் 2) உள்ளூர் அதிகாரிகளை தொடர்பு கொள்ளுங்கள் 3) பயிர் காப்பீட்டை சரிபார்க்கவும்",
                "en": "Multiple disasters advice: 1) Take immediate safety measures 2) Contact local authorities 3) Check crop insurance"
            }
        }
    
    def process_query(self, query: str, location: str, language: str) -> str:
        """
        Process a weather-related query and generate a response.
        
        Args:
            query: User query text
            location: Location for weather data (e.g., "bangalore", "mumbai")
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Formatted response string with weather information and mitigation advice
        
        Validates Requirements: 3.1
        """
        # Fetch weather data for the location
        weather = self.fetch_weather_data(location)
        
        if weather is None:
            # Return a localized message if location not found
            no_data_messages = {
                "hi": f"क्षमा करें, {location} के लिए मौसम डेटा उपलब्ध नहीं है।",
                "kn": f"ಕ್ಷಮಿಸಿ, {location} ಗೆ ಹವಾಮಾನ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ.",
                "ta": f"மன்னிக்கவும், {location} க்கான வானிலை தரவு கிடைக்கவில்லை.",
                "en": f"Sorry, weather data not available for {location}."
            }
            return no_data_messages.get(language, no_data_messages["en"])
        
        # Build weather summary
        weather_summary = self._format_weather_summary(weather, language)
        
        # Check for disaster conditions and add mitigation steps if needed
        has_disaster = self.detect_disaster_conditions(weather)
        
        if has_disaster:
            disaster_type = self._determine_disaster_type(weather)
            mitigation = self.generate_mitigation_steps(disaster_type, language)
            response = f"{weather_summary}\n\n{mitigation}"
        else:
            response = weather_summary
        
        return response
    
    def fetch_weather_data(self, location: str) -> Optional[WeatherData]:
        """
        Fetch weather data for a specific location.
        
        For MVP, this returns hardcoded mock data. In production, this would call
        an external weather API.
        
        Args:
            location: Location name (e.g., "bangalore", "mumbai")
        
        Returns:
            WeatherData object or None if location not found
        
        Validates Requirements: 3.3
        """
        # Normalize location name (lowercase, strip whitespace)
        location_key = location.lower().strip()
        
        # Return mock data if available
        return self.mock_weather_data.get(location_key)
    
    def detect_disaster_conditions(self, weather: WeatherData) -> bool:
        """
        Detect if weather data indicates disaster conditions.
        
        Disaster detection rules:
        - Heavy rainfall: > 100mm in 24 hours
        - High temperature: > 40°C
        - Strong winds: > 50 km/h
        
        Args:
            weather: WeatherData object to check
        
        Returns:
            True if disaster conditions detected, False otherwise
        
        Validates Requirements: 3.4
        """
        # Check each disaster threshold
        heavy_rain = weather.rainfall_mm > 100.0
        high_temp = weather.temperature_celsius > 40.0
        strong_wind = weather.wind_speed_kmh > 50.0
        
        # Return True if any disaster condition is met
        return heavy_rain or high_temp or strong_wind
    
    def generate_mitigation_steps(self, disaster_type: str, language: str) -> str:
        """
        Generate localized mitigation advice for a specific disaster type.
        
        Args:
            disaster_type: Type of disaster ("heavy_rain", "heat_wave", "strong_wind", "multiple")
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Localized mitigation advice string
        
        Validates Requirements: 3.4
        """
        # Get mitigation steps for the disaster type and language
        if disaster_type in self.mitigation_steps:
            steps = self.mitigation_steps[disaster_type]
            return steps.get(language, steps.get("en", ""))
        
        # Fallback to generic advice
        return self.mitigation_steps["multiple"].get(language, self.mitigation_steps["multiple"]["en"])
    
    def _determine_disaster_type(self, weather: WeatherData) -> str:
        """
        Determine the primary disaster type from weather data.
        
        Args:
            weather: WeatherData object
        
        Returns:
            Disaster type string ("heavy_rain", "heat_wave", "strong_wind", "multiple")
        """
        disaster_count = 0
        disaster_type = "multiple"
        
        # Check each condition
        if weather.rainfall_mm > 100.0:
            disaster_count += 1
            disaster_type = "heavy_rain"
        
        if weather.temperature_celsius > 40.0:
            disaster_count += 1
            disaster_type = "heat_wave"
        
        if weather.wind_speed_kmh > 50.0:
            disaster_count += 1
            disaster_type = "strong_wind"
        
        # If multiple conditions, return "multiple"
        if disaster_count > 1:
            return "multiple"
        
        return disaster_type
    
    def _format_weather_summary(self, weather: WeatherData, language: str) -> str:
        """
        Format weather data into a localized summary string.
        
        Args:
            weather: WeatherData object
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Formatted weather summary string
        """
        templates = {
            "hi": f"{weather.location} का मौसम: तापमान {weather.temperature_celsius}°C, आर्द्रता {weather.humidity_percent}%, वर्षा {weather.rainfall_mm}mm, हवा {weather.wind_speed_kmh} km/h। स्थिति: {weather.weather_condition}।",
            "kn": f"{weather.location} ಹವಾಮಾನ: ತಾಪಮಾನ {weather.temperature_celsius}°C, ತೇವಾಂಶ {weather.humidity_percent}%, ಮಳೆ {weather.rainfall_mm}mm, ಗಾಳಿ {weather.wind_speed_kmh} km/h. ಸ್ಥಿತಿ: {weather.weather_condition}.",
            "ta": f"{weather.location} வானிலை: வெப்பநிலை {weather.temperature_celsius}°C, ஈரப்பதம் {weather.humidity_percent}%, மழை {weather.rainfall_mm}mm, காற்று {weather.wind_speed_kmh} km/h. நிலை: {weather.weather_condition}.",
            "en": f"{weather.location} weather: Temperature {weather.temperature_celsius}°C, Humidity {weather.humidity_percent}%, Rainfall {weather.rainfall_mm}mm, Wind {weather.wind_speed_kmh} km/h. Condition: {weather.weather_condition}."
        }
        
        return templates.get(language, templates["en"])
