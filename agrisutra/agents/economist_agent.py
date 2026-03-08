"""
Economist Agent - Crop Budgeting and ROI Query Handler

This module implements the Economist Agent that handles crop budgeting and ROI calculations.
For the MVP, it uses hardcoded crop costs, yields, and market prices instead of calling external APIs.

Validates Requirements: 3.2, 3.5
"""

from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ROIEstimate:
    """ROI estimate model for a specific crop"""
    crop: str
    area: float
    total_cost: float
    expected_yield: float
    expected_revenue: float
    roi_percentage: float
    breakeven_price: float


@dataclass
class MarketData:
    """Market data model for a specific crop"""
    crop: str
    location: str
    timestamp: datetime
    current_price_per_kg: float
    price_trend: str  # "rising" | "falling" | "stable"
    demand_level: str  # "low" | "medium" | "high"
    source: str  # "api" | "cache" | "mock"


class EconomistAgent:
    """
    Economist Agent handles crop budgeting and ROI calculations.
    
    For the MVP, this agent uses hardcoded crop costs, yields, and market prices
    for demonstration purposes.
    """
    
    def __init__(self):
        """Initialize the Economist Agent with mock crop and market data"""
        self._initialize_crop_data()
        self._initialize_market_data()
    
    def _initialize_crop_data(self):
        """Initialize hardcoded crop input costs and yield estimates"""
        # Costs are per acre in INR
        # Yields are in kg per acre
        self.crop_data = {
            "rice": {
                "seed_cost": 2000,
                "fertilizer_cost": 3500,
                "pesticide_cost": 1500,
                "labor_cost": 8000,
                "irrigation_cost": 2500,
                "other_cost": 1500,
                "expected_yield_kg": 2500,
                "names": {
                    "hi": "चावल",
                    "kn": "ಅಕ್ಕಿ",
                    "ta": "அரிசி",
                    "en": "Rice"
                }
            },
            "wheat": {
                "seed_cost": 1800,
                "fertilizer_cost": 3000,
                "pesticide_cost": 1200,
                "labor_cost": 7000,
                "irrigation_cost": 2000,
                "other_cost": 1000,
                "expected_yield_kg": 2000,
                "names": {
                    "hi": "गेहूं",
                    "kn": "ಗೋಧಿ",
                    "ta": "கோதுமை",
                    "en": "Wheat"
                }
            },
            "cotton": {
                "seed_cost": 2500,
                "fertilizer_cost": 4000,
                "pesticide_cost": 3000,
                "labor_cost": 9000,
                "irrigation_cost": 3000,
                "other_cost": 2000,
                "expected_yield_kg": 1500,
                "names": {
                    "hi": "कपास",
                    "kn": "ಹತ್ತಿ",
                    "ta": "பருத்தி",
                    "en": "Cotton"
                }
            },
            "sugarcane": {
                "seed_cost": 5000,
                "fertilizer_cost": 6000,
                "pesticide_cost": 2500,
                "labor_cost": 12000,
                "irrigation_cost": 4000,
                "other_cost": 3000,
                "expected_yield_kg": 40000,
                "names": {
                    "hi": "गन्ना",
                    "kn": "ಕಬ್ಬು",
                    "ta": "கரும்பு",
                    "en": "Sugarcane"
                }
            },
            "maize": {
                "seed_cost": 1500,
                "fertilizer_cost": 2500,
                "pesticide_cost": 1000,
                "labor_cost": 6000,
                "irrigation_cost": 1500,
                "other_cost": 1000,
                "expected_yield_kg": 2200,
                "names": {
                    "hi": "मक्का",
                    "kn": "ಜೋಳ",
                    "ta": "சோளம்",
                    "en": "Maize"
                }
            },
            "tomato": {
                "seed_cost": 3000,
                "fertilizer_cost": 4500,
                "pesticide_cost": 2500,
                "labor_cost": 10000,
                "irrigation_cost": 3500,
                "other_cost": 2500,
                "expected_yield_kg": 8000,
                "names": {
                    "hi": "टमाटर",
                    "kn": "ಟೊಮೇಟೊ",
                    "ta": "தக்காளி",
                    "en": "Tomato"
                }
            },
            "potato": {
                "seed_cost": 4000,
                "fertilizer_cost": 3500,
                "pesticide_cost": 2000,
                "labor_cost": 8500,
                "irrigation_cost": 2500,
                "other_cost": 2000,
                "expected_yield_kg": 6000,
                "names": {
                    "hi": "आलू",
                    "kn": "ಆಲೂಗಡ್ಡೆ",
                    "ta": "உருளைக்கிழங்கு",
                    "en": "Potato"
                }
            },
            "onion": {
                "seed_cost": 2500,
                "fertilizer_cost": 3000,
                "pesticide_cost": 1800,
                "labor_cost": 7500,
                "irrigation_cost": 2000,
                "other_cost": 1500,
                "expected_yield_kg": 5000,
                "names": {
                    "hi": "प्याज",
                    "kn": "ಈರುಳ್ಳಿ",
                    "ta": "வெங்காயம்",
                    "en": "Onion"
                }
            }
        }
    
    def _initialize_market_data(self):
        """Initialize hardcoded market prices for demo crops"""
        self.market_data = {
            "rice": MarketData(
                crop="rice",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=25.0,
                price_trend="stable",
                demand_level="high",
                source="mock"
            ),
            "wheat": MarketData(
                crop="wheat",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=22.0,
                price_trend="rising",
                demand_level="high",
                source="mock"
            ),
            "cotton": MarketData(
                crop="cotton",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=60.0,
                price_trend="stable",
                demand_level="medium",
                source="mock"
            ),
            "sugarcane": MarketData(
                crop="sugarcane",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=3.5,
                price_trend="stable",
                demand_level="high",
                source="mock"
            ),
            "maize": MarketData(
                crop="maize",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=18.0,
                price_trend="rising",
                demand_level="medium",
                source="mock"
            ),
            "tomato": MarketData(
                crop="tomato",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=15.0,
                price_trend="falling",
                demand_level="high",
                source="mock"
            ),
            "potato": MarketData(
                crop="potato",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=12.0,
                price_trend="stable",
                demand_level="high",
                source="mock"
            ),
            "onion": MarketData(
                crop="onion",
                location="National Average",
                timestamp=datetime.now(),
                current_price_per_kg=20.0,
                price_trend="rising",
                demand_level="high",
                source="mock"
            )
        }
    
    def process_query(self, query: str, crop: str, area: float, language: str) -> str:
        """
        Process a crop finance query and generate a response with ROI calculation.
        
        Args:
            query: User query text
            crop: Crop name (e.g., "rice", "wheat", "cotton")
            area: Farm area in acres
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Formatted response string with ROI estimate and market information
        
        Validates Requirements: 3.2
        """
        # Normalize crop name
        crop_key = crop.lower().strip()
        
        # Check if crop data is available
        if crop_key not in self.crop_data:
            return self._format_unknown_crop_message(crop, language)
        
        # Calculate ROI
        roi_estimate = self.calculate_roi(crop_key, area)
        
        if roi_estimate is None:
            return self._format_calculation_error_message(language)
        
        # Fetch market prices
        market_data = self.fetch_market_prices(crop_key)
        
        # Format response
        response = self._format_roi_response(roi_estimate, market_data, language)
        
        return response
    
    def calculate_roi(self, crop: str, area: float, inputs: Optional[Dict] = None) -> Optional[ROIEstimate]:
        """
        Calculate ROI estimate for a specific crop and area.
        
        For MVP, this uses hardcoded crop costs and yields. The inputs parameter
        is optional and allows custom cost overrides (not used in MVP).
        
        Args:
            crop: Crop name (e.g., "rice", "wheat")
            area: Farm area in acres
            inputs: Optional dictionary of custom input costs (not used in MVP)
        
        Returns:
            ROIEstimate object or None if crop not found
        
        Validates Requirements: 3.5
        """
        # Get crop data
        if crop not in self.crop_data:
            return None
        
        crop_info = self.crop_data[crop]
        
        # Calculate total cost per acre
        cost_per_acre = (
            crop_info["seed_cost"] +
            crop_info["fertilizer_cost"] +
            crop_info["pesticide_cost"] +
            crop_info["labor_cost"] +
            crop_info["irrigation_cost"] +
            crop_info["other_cost"]
        )
        
        # Calculate total cost for given area
        total_cost = cost_per_acre * area
        
        # Calculate expected yield
        expected_yield = crop_info["expected_yield_kg"] * area
        
        # Get market price
        market_data = self.fetch_market_prices(crop)
        if market_data is None:
            return None
        
        current_price = market_data.current_price_per_kg
        
        # Calculate expected revenue
        expected_revenue = expected_yield * current_price
        
        # Calculate ROI percentage
        if total_cost > 0:
            roi_percentage = ((expected_revenue - total_cost) / total_cost) * 100
        else:
            roi_percentage = 0.0
        
        # Calculate breakeven price
        if expected_yield > 0:
            breakeven_price = total_cost / expected_yield
        else:
            breakeven_price = 0.0
        
        return ROIEstimate(
            crop=crop,
            area=area,
            total_cost=total_cost,
            expected_yield=expected_yield,
            expected_revenue=expected_revenue,
            roi_percentage=roi_percentage,
            breakeven_price=breakeven_price
        )
    
    def fetch_market_prices(self, crop: str) -> Optional[MarketData]:
        """
        Fetch current market prices for a specific crop.
        
        For MVP, this returns hardcoded mock data. In production, this would call
        an external market data API.
        
        Args:
            crop: Crop name (e.g., "rice", "wheat")
        
        Returns:
            MarketData object or None if crop not found
        
        Validates Requirements: 3.5
        """
        # Normalize crop name
        crop_key = crop.lower().strip()
        
        # Return mock market data if available
        return self.market_data.get(crop_key)
    
    def _format_roi_response(self, roi: ROIEstimate, market: Optional[MarketData], language: str) -> str:
        """
        Format ROI estimate and market data into a localized response string.
        
        Args:
            roi: ROIEstimate object
            market: MarketData object (optional)
            language: Language code (hi, kn, ta, en)
        
        Returns:
            Formatted response string
        """
        crop_name = self.crop_data[roi.crop]["names"].get(language, roi.crop)
        
        # Format numbers with Indian numbering system (lakhs)
        cost_str = f"₹{roi.total_cost:,.0f}"
        revenue_str = f"₹{roi.expected_revenue:,.0f}"
        yield_str = f"{roi.expected_yield:,.0f}"
        roi_str = f"{roi.roi_percentage:.1f}%"
        breakeven_str = f"₹{roi.breakeven_price:.2f}"
        
        templates = {
            "hi": (
                f"{crop_name} ({roi.area} एकड़) के लिए बजट:\n"
                f"कुल लागत: {cost_str}\n"
                f"अपेक्षित उपज: {yield_str} kg\n"
                f"अपेक्षित आय: {revenue_str}\n"
                f"ROI: {roi_str}\n"
                f"ब्रेकईवन मूल्य: {breakeven_str}/kg"
            ),
            "kn": (
                f"{crop_name} ({roi.area} ಎಕರೆ) ಗೆ ಬಜೆಟ್:\n"
                f"ಒಟ್ಟು ವೆಚ್ಚ: {cost_str}\n"
                f"ನಿರೀಕ್ಷಿತ ಇಳುವರಿ: {yield_str} kg\n"
                f"ನಿರೀಕ್ಷಿತ ಆದಾಯ: {revenue_str}\n"
                f"ROI: {roi_str}\n"
                f"ಬ್ರೇಕ್‌ಈವನ್ ಬೆಲೆ: {breakeven_str}/kg"
            ),
            "ta": (
                f"{crop_name} ({roi.area} ஏக்கர்) க்கான பட்ஜெட்:\n"
                f"மொத்த செலவு: {cost_str}\n"
                f"எதிர்பார்க்கப்படும் விளைச்சல்: {yield_str} kg\n"
                f"எதிர்பார்க்கப்படும் வருமானம்: {revenue_str}\n"
                f"ROI: {roi_str}\n"
                f"பிரேக்இவன் விலை: {breakeven_str}/kg"
            ),
            "en": (
                f"Budget for {crop_name} ({roi.area} acres):\n"
                f"Total cost: {cost_str}\n"
                f"Expected yield: {yield_str} kg\n"
                f"Expected revenue: {revenue_str}\n"
                f"ROI: {roi_str}\n"
                f"Breakeven price: {breakeven_str}/kg"
            )
        }
        
        response = templates.get(language, templates["en"])
        
        # Add market information if available
        if market:
            price_str = f"₹{market.current_price_per_kg:.2f}"
            
            market_templates = {
                "hi": f"\n\nबाजार मूल्य: {price_str}/kg ({market.price_trend}), मांग: {market.demand_level}",
                "kn": f"\n\nಮಾರುಕಟ್ಟೆ ಬೆಲೆ: {price_str}/kg ({market.price_trend}), ಬೇಡಿಕೆ: {market.demand_level}",
                "ta": f"\n\nசந்தை விலை: {price_str}/kg ({market.price_trend}), தேவை: {market.demand_level}",
                "en": f"\n\nMarket price: {price_str}/kg ({market.price_trend}), Demand: {market.demand_level}"
            }
            
            response += market_templates.get(language, market_templates["en"])
        
        return response
    
    def _format_unknown_crop_message(self, crop: str, language: str) -> str:
        """Format a localized message for unknown crop"""
        templates = {
            "hi": f"क्षमा करें, {crop} के लिए डेटा उपलब्ध नहीं है। कृपया चावल, गेहूं, कपास, गन्ना, मक्का, टमाटर, आलू, या प्याज में से चुनें।",
            "kn": f"ಕ್ಷಮಿಸಿ, {crop} ಗೆ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಅಕ್ಕಿ, ಗೋಧಿ, ಹತ್ತಿ, ಕಬ್ಬು, ಜೋಳ, ಟೊಮೇಟೊ, ಆಲೂಗಡ್ಡೆ, ಅಥವಾ ಈರುಳ್ಳಿ ಆಯ್ಕೆಮಾಡಿ.",
            "ta": f"மன்னிக்கவும், {crop} க்கான தரவு கிடைக்கவில்லை. தயவுசெய்து அரிசி, கோதுமை, பருத்தி, கரும்பு, சோளம், தக்காளி, உருளைக்கிழங்கு, அல்லது வெங்காயம் தேர்ந்தெடுக்கவும்.",
            "en": f"Sorry, data not available for {crop}. Please choose from rice, wheat, cotton, sugarcane, maize, tomato, potato, or onion."
        }
        return templates.get(language, templates["en"])
    
    def _format_calculation_error_message(self, language: str) -> str:
        """Format a localized message for calculation errors"""
        templates = {
            "hi": "क्षमा करें, ROI गणना में त्रुटि हुई। कृपया फिर से प्रयास करें।",
            "kn": "ಕ್ಷಮಿಸಿ, ROI ಲೆಕ್ಕಾಚಾರದಲ್ಲಿ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
            "ta": "மன்னிக்கவும், ROI கணக்கீட்டில் பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
            "en": "Sorry, error in ROI calculation. Please try again."
        }
        return templates.get(language, templates["en"])
