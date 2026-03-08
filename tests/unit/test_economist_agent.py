"""
Unit tests for Economist Agent

Tests the crop budgeting and ROI calculation functionality of the Economist Agent.
Validates Requirements: 3.2, 3.5
"""

import pytest
from datetime import datetime
from agrisutra.agents.economist_agent import EconomistAgent, ROIEstimate, MarketData


class TestEconomistAgent:
    """Test suite for EconomistAgent class"""
    
    @pytest.fixture
    def agent(self):
        """Create an EconomistAgent instance for testing"""
        return EconomistAgent()
    
    def test_initialization(self, agent):
        """Test that EconomistAgent initializes correctly"""
        assert agent is not None
        assert hasattr(agent, 'crop_data')
        assert hasattr(agent, 'market_data')
        assert len(agent.crop_data) >= 5
        assert len(agent.market_data) >= 5
    
    def test_fetch_market_prices_valid_crop(self, agent):
        """Test fetching market prices for a valid crop"""
        market = agent.fetch_market_prices("rice")
        assert market is not None
        assert isinstance(market, MarketData)
        assert market.crop == "rice"
        assert market.current_price_per_kg > 0
        assert market.source == "mock"
    
    def test_fetch_market_prices_case_insensitive(self, agent):
        """Test that crop lookup is case-insensitive"""
        market1 = agent.fetch_market_prices("RICE")
        market2 = agent.fetch_market_prices("rice")
        market3 = agent.fetch_market_prices("Rice")
        
        assert market1 is not None
        assert market2 is not None
        assert market3 is not None
        assert market1.crop == market2.crop == market3.crop
    
    def test_fetch_market_prices_invalid_crop(self, agent):
        """Test fetching market prices for an invalid crop"""
        market = agent.fetch_market_prices("nonexistent_crop")
        assert market is None
    
    def test_calculate_roi_valid_crop(self, agent):
        """Test ROI calculation for a valid crop"""
        roi = agent.calculate_roi("rice", area=2.0)
        
        assert roi is not None
        assert isinstance(roi, ROIEstimate)
        assert roi.crop == "rice"
        assert roi.area == 2.0
        assert roi.total_cost > 0
        assert roi.expected_yield > 0
        assert roi.expected_revenue > 0
        assert roi.breakeven_price > 0
    
    def test_calculate_roi_invalid_crop(self, agent):
        """Test ROI calculation for an invalid crop"""
        roi = agent.calculate_roi("invalid_crop", area=1.0)
        assert roi is None
    
    def test_calculate_roi_zero_area(self, agent):
        """Test ROI calculation with zero area"""
        roi = agent.calculate_roi("rice", area=0.0)
        
        assert roi is not None
        assert roi.total_cost == 0.0
        assert roi.expected_yield == 0.0
    
    def test_calculate_roi_large_area(self, agent):
        """Test ROI calculation with large area"""
        roi = agent.calculate_roi("wheat", area=10.0)
        
        assert roi is not None
        assert roi.area == 10.0
        # Total cost should scale with area
        roi_1_acre = agent.calculate_roi("wheat", area=1.0)
        assert roi.total_cost == pytest.approx(roi_1_acre.total_cost * 10, rel=0.01)
    
    def test_calculate_roi_profitability(self, agent):
        """Test that ROI calculation correctly determines profitability"""
        roi = agent.calculate_roi("rice", area=1.0)
        
        assert roi is not None
        # ROI percentage should be calculated correctly
        expected_roi = ((roi.expected_revenue - roi.total_cost) / roi.total_cost) * 100
        assert roi.roi_percentage == pytest.approx(expected_roi, rel=0.01)
    
    def test_calculate_roi_breakeven_price(self, agent):
        """Test that breakeven price is calculated correctly"""
        roi = agent.calculate_roi("wheat", area=1.0)
        
        assert roi is not None
        # Breakeven price should be total cost / expected yield
        expected_breakeven = roi.total_cost / roi.expected_yield
        assert roi.breakeven_price == pytest.approx(expected_breakeven, rel=0.01)
    
    def test_process_query_valid_crop(self, agent):
        """Test processing a query for a valid crop"""
        response = agent.process_query(
            query="What is the budget for rice?",
            crop="rice",
            area=2.0,
            language="en"
        )
        
        assert response is not None
        assert "Rice" in response or "rice" in response
        assert "2" in response  # Area
        assert "₹" in response  # Currency symbol
        assert "ROI" in response
    
    def test_process_query_invalid_crop(self, agent):
        """Test processing a query for an invalid crop"""
        response = agent.process_query(
            query="What is the budget?",
            crop="invalid_crop",
            area=1.0,
            language="en"
        )
        
        assert response is not None
        assert "not available" in response.lower() or "sorry" in response.lower()
    
    def test_process_query_localized_hindi(self, agent):
        """Test processing a query with Hindi language"""
        response = agent.process_query(
            query="चावल का बजट क्या है?",
            crop="rice",
            area=1.0,
            language="hi"
        )
        
        assert response is not None
        assert "चावल" in response
        assert "₹" in response
        assert "लागत" in response or "आय" in response
    
    def test_process_query_localized_kannada(self, agent):
        """Test processing a query with Kannada language"""
        response = agent.process_query(
            query="ಗೋಧಿ ಬಜೆಟ್ ಏನು?",
            crop="wheat",
            area=1.0,
            language="kn"
        )
        
        assert response is not None
        assert "ಗೋಧಿ" in response
        assert "₹" in response
        assert "ವೆಚ್ಚ" in response or "ಆದಾಯ" in response
    
    def test_process_query_localized_tamil(self, agent):
        """Test processing a query with Tamil language"""
        response = agent.process_query(
            query="பருத்தி பட்ஜெட் என்ன?",
            crop="cotton",
            area=1.0,
            language="ta"
        )
        
        assert response is not None
        assert "பருத்தி" in response
        assert "₹" in response
        assert "செலவு" in response or "வருமானம்" in response
    
    def test_process_query_includes_market_data(self, agent):
        """Test that query response includes market data"""
        response = agent.process_query(
            query="What is the budget for tomato?",
            crop="tomato",
            area=1.0,
            language="en"
        )
        
        assert response is not None
        assert "Market price" in response or "market" in response.lower()
        assert "Demand" in response or "demand" in response.lower()
    
    def test_crop_data_completeness(self, agent):
        """Test that crop data has all required fields"""
        for crop_name, crop_info in agent.crop_data.items():
            assert "seed_cost" in crop_info
            assert "fertilizer_cost" in crop_info
            assert "pesticide_cost" in crop_info
            assert "labor_cost" in crop_info
            assert "irrigation_cost" in crop_info
            assert "other_cost" in crop_info
            assert "expected_yield_kg" in crop_info
            assert "names" in crop_info
            
            # Check that names exist for all languages
            assert "hi" in crop_info["names"]
            assert "kn" in crop_info["names"]
            assert "ta" in crop_info["names"]
            assert "en" in crop_info["names"]
    
    def test_market_data_completeness(self, agent):
        """Test that market data has all required fields"""
        for crop_name, market_info in agent.market_data.items():
            assert isinstance(market_info, MarketData)
            assert market_info.crop == crop_name
            assert market_info.current_price_per_kg > 0
            assert market_info.price_trend in ["rising", "falling", "stable"]
            assert market_info.demand_level in ["low", "medium", "high"]
            assert market_info.source == "mock"
    
    def test_multiple_crops_coverage(self, agent):
        """Test that agent supports multiple crop types"""
        crops = ["rice", "wheat", "cotton", "sugarcane", "maize", "tomato", "potato", "onion"]
        
        for crop in crops:
            roi = agent.calculate_roi(crop, area=1.0)
            assert roi is not None, f"ROI calculation failed for {crop}"
            assert roi.crop == crop
    
    def test_roi_estimate_dataclass(self):
        """Test ROIEstimate dataclass structure"""
        roi = ROIEstimate(
            crop="test",
            area=1.0,
            total_cost=10000.0,
            expected_yield=1000.0,
            expected_revenue=15000.0,
            roi_percentage=50.0,
            breakeven_price=10.0
        )
        
        assert roi.crop == "test"
        assert roi.area == 1.0
        assert roi.total_cost == 10000.0
        assert roi.expected_yield == 1000.0
        assert roi.expected_revenue == 15000.0
        assert roi.roi_percentage == 50.0
        assert roi.breakeven_price == 10.0
    
    def test_market_data_dataclass(self):
        """Test MarketData dataclass structure"""
        market = MarketData(
            crop="test",
            location="Test Location",
            timestamp=datetime.now(),
            current_price_per_kg=20.0,
            price_trend="stable",
            demand_level="high",
            source="mock"
        )
        
        assert market.crop == "test"
        assert market.location == "Test Location"
        assert market.current_price_per_kg == 20.0
        assert market.price_trend == "stable"
        assert market.demand_level == "high"
        assert market.source == "mock"
    
    def test_response_formatting_includes_all_info(self, agent):
        """Test that response includes all relevant information"""
        response = agent.process_query(
            query="Budget for rice",
            crop="rice",
            area=1.5,
            language="en"
        )
        
        assert response is not None
        # Should include crop name
        assert "Rice" in response or "rice" in response
        # Should include area
        assert "1.5" in response
        # Should include cost
        assert "cost" in response.lower() or "₹" in response
        # Should include yield
        assert "yield" in response.lower() or "kg" in response
        # Should include revenue
        assert "revenue" in response.lower() or "income" in response.lower()
        # Should include ROI
        assert "ROI" in response or "%" in response
        # Should include breakeven
        assert "breakeven" in response.lower() or "Breakeven" in response
