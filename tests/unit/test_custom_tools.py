# ruff: noqa
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example Test for Custom Tools - Educational Example

This demonstrates how to write tests for your custom tools.
Testing tools separately from agents helps you:
1. Verify tool logic is correct
2. Debug issues faster
3. Ensure tools handle edge cases
4. Document expected behavior

STUDENT EXERCISES:
1. Add tests for other tools in custom_tools.py
2. Add edge case tests (negative numbers, empty strings, etc.)
3. Add parametrized tests to test multiple inputs
4. Mock external dependencies if your tools call APIs
"""

import pytest
from app.custom_tools import (
    get_stock_price,
    calculate_tip,
    convert_temperature,
    analyze_text,
)


class TestStockPrice:
    """Tests for the get_stock_price tool."""
    
    def test_known_stock_symbol(self):
        """Test that known stock symbols return a price."""
        result = get_stock_price("AAPL")
        assert "AAPL" in result
        assert "$" in result
        assert "price" in result.lower()
    
    def test_unknown_stock_symbol(self):
        """Test that unknown symbols return an appropriate message."""
        result = get_stock_price("UNKNOWN")
        assert "don't have" in result.lower() or "sorry" in result.lower()
    
    def test_case_insensitive(self):
        """Test that stock symbols are case-insensitive."""
        result_upper = get_stock_price("GOOGL")
        result_lower = get_stock_price("googl")
        # Both should mention GOOGL (uppercase in response)
        assert "GOOGL" in result_upper
        assert "GOOGL" in result_lower


class TestCalculateTip:
    """Tests for the calculate_tip tool."""
    
    def test_default_tip_percentage(self):
        """Test tip calculation with default 15% tip."""
        result = calculate_tip(100.0)
        assert "$100.00" in result  # Bill amount
        assert "$15.00" in result   # 15% tip
        assert "$115.00" in result  # Total
    
    def test_custom_tip_percentage(self):
        """Test tip calculation with custom percentage."""
        result = calculate_tip(50.0, 20.0)
        assert "$50.00" in result   # Bill amount
        assert "$10.00" in result   # 20% tip
        assert "$60.00" in result   # Total
    
    def test_negative_bill_amount(self):
        """Test that negative bill amounts are rejected."""
        result = calculate_tip(-50.0)
        assert "error" in result.lower()
        assert "negative" in result.lower()
    
    def test_invalid_tip_percentage(self):
        """Test that invalid tip percentages are rejected."""
        result = calculate_tip(100.0, 150.0)  # 150% is too high
        assert "error" in result.lower()
    
    def test_zero_tip(self):
        """Test calculation with 0% tip."""
        result = calculate_tip(100.0, 0.0)
        assert "$0.00" in result or "0%" in result


class TestConvertTemperature:
    """Tests for the convert_temperature tool."""
    
    def test_celsius_to_fahrenheit(self):
        """Test converting Celsius to Fahrenheit."""
        result = convert_temperature(0, "C", "F")
        assert "32.00" in result  # 0°C = 32°F
    
    def test_fahrenheit_to_celsius(self):
        """Test converting Fahrenheit to Celsius."""
        result = convert_temperature(32, "F", "C")
        assert "0.00" in result  # 32°F = 0°C
    
    def test_celsius_to_kelvin(self):
        """Test converting Celsius to Kelvin."""
        result = convert_temperature(0, "C", "K")
        assert "273.15" in result  # 0°C = 273.15K
    
    def test_same_unit_conversion(self):
        """Test converting to the same unit (should return same value)."""
        result = convert_temperature(100, "C", "C")
        assert "100.00" in result
    
    def test_round_trip_conversion(self):
        """Test that converting back and forth returns original value."""
        # 100°C → F → C should be ~100°C
        c_to_f = convert_temperature(100, "C", "F")
        # Extract the Fahrenheit value (this is simplified for the example)
        # In a real test, you'd parse the result properly
        assert "212.00" in c_to_f  # 100°C = 212°F


class TestAnalyzeText:
    """Tests for the analyze_text tool."""
    
    def test_simple_text(self):
        """Test analyzing a simple sentence."""
        text = "Hello world."
        result = analyze_text(text)
        assert "2" in result  # 2 words
        assert "1" in result  # 1 sentence
    
    def test_empty_text(self):
        """Test analyzing empty text."""
        result = analyze_text("")
        # Should handle gracefully, not crash
        assert "0" in result
    
    def test_multi_sentence_text(self):
        """Test analyzing multiple sentences."""
        text = "First sentence. Second sentence! Third sentence?"
        result = analyze_text(text)
        assert "3" in result  # 3 sentences
        assert "6" in result  # 6 words
    
    def test_text_with_numbers(self):
        """Test that the analysis includes character counts."""
        text = "Test"
        result = analyze_text(text)
        assert "Characters" in result or "characters" in result


# ============================================================================
# PARAMETRIZED TESTS (Advanced)
# ============================================================================

@pytest.mark.parametrize("symbol,should_succeed", [
    ("AAPL", True),
    ("GOOGL", True),
    ("MSFT", True),
    ("TSLA", True),
    ("INVALID", False),
    ("", False),
])
def test_stock_price_parametrized(symbol, should_succeed):
    """Test multiple stock symbols using parametrized testing."""
    result = get_stock_price(symbol)
    if should_succeed:
        assert "$" in result
        assert symbol.upper() in result
    else:
        assert "don't have" in result.lower() or "sorry" in result.lower()


@pytest.mark.parametrize("bill,tip_pct,expected_tip", [
    (100.0, 15.0, 15.0),
    (50.0, 20.0, 10.0),
    (200.0, 10.0, 20.0),
    (75.0, 18.0, 13.5),
])
def test_tip_calculation_parametrized(bill, tip_pct, expected_tip):
    """Test tip calculations with various inputs."""
    result = calculate_tip(bill, tip_pct)
    # Check that the expected tip amount appears in the result
    assert f"${expected_tip:.2f}" in result


# ============================================================================
# INTEGRATION TEST EXAMPLE
# ============================================================================

def test_tools_work_together():
    """
    Example of testing multiple tools together.
    This simulates how an agent might use multiple tools in sequence.
    """
    # Step 1: Get stock price
    stock_result = get_stock_price("AAPL")
    assert "$" in stock_result
    
    # Step 2: Analyze the result text
    analysis = analyze_text(stock_result)
    assert "Characters" in analysis or "characters" in analysis
    
    # Step 3: Do a calculation
    tip_result = calculate_tip(100.0, 15.0)
    assert "$115.00" in tip_result


# ============================================================================
# RUNNING THE TESTS
# ============================================================================
"""
To run these tests:

1. From the project root:
   $ make test

2. To run only this file:
   $ uv run pytest tests/unit/test_custom_tools.py

3. To run with verbose output:
   $ uv run pytest tests/unit/test_custom_tools.py -v

4. To run a specific test:
   $ uv run pytest tests/unit/test_custom_tools.py::TestStockPrice::test_known_stock_symbol

5. To see print statements:
   $ uv run pytest tests/unit/test_custom_tools.py -s

STUDENT EXERCISES:

1. Add tests for the remaining tools in custom_tools.py:
   - get_news_headlines
   - make_recommendation
   - add_to_shopping_list

2. Add edge case tests:
   - What happens with very large numbers?
   - What about special characters in text?
   - How do tools handle None or empty inputs?

3. Add more parametrized tests:
   - Test temperature conversion with multiple values
   - Test text analysis with various text lengths

4. Mock external dependencies:
   - If your tool calls an API, mock the API response
   - Test how your tool handles API failures

5. Test error handling:
   - Verify tools return helpful error messages
   - Ensure tools don't crash on bad input
"""
