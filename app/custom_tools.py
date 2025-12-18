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
Custom Tools for ADK Agents - Educational Examples

This module contains simple tool examples that students can use as templates
for creating their own custom tools. Each tool demonstrates different patterns
and best practices.

STUDENT EXERCISE IDEAS:
1. Modify existing tools to add new functionality
2. Create new tools for different domains (finance, sports, etc.)
3. Add error handling and validation
4. Combine multiple tools in creative ways
"""

import random
from typing import Literal


# ============================================================================
# SIMPLE DATA RETRIEVAL TOOLS
# ============================================================================

def get_stock_price(symbol: str) -> str:
    """Simulates getting a stock price for a given symbol.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        
    Returns:
        A string with simulated stock price information.
        
    STUDENT EXERCISE:
    - Add support for multiple stock symbols
    - Return structured data (dict) instead of string
    - Add historical price trends
    """
    prices = {
        "AAPL": 178.50,
        "GOOGL": 142.30,
        "MSFT": 380.20,
        "TSLA": 245.60,
    }
    
    symbol_upper = symbol.upper()
    if symbol_upper in prices:
        price = prices[symbol_upper] + random.uniform(-5, 5)  # Add some variation
        return f"The current price of {symbol_upper} is ${price:.2f}"
    else:
        return f"Sorry, I don't have price information for {symbol}. Try AAPL, GOOGL, MSFT, or TSLA."


def get_news_headlines(topic: str, num_headlines: int = 3) -> str:
    """Simulates fetching news headlines for a given topic.
    
    Args:
        topic: The news topic to search for
        num_headlines: Number of headlines to return (default: 3)
        
    Returns:
        A formatted string with simulated news headlines.
        
    STUDENT EXERCISE:
    - Add date/time to headlines
    - Categorize news by sentiment (positive/negative/neutral)
    - Add source attribution
    """
    headlines_db = {
        "technology": [
            "New AI breakthrough announced by major tech company",
            "Smartphone sales reach record high in Q4",
            "Cybersecurity experts warn of new threat",
            "Tech giant launches revolutionary product",
        ],
        "sports": [
            "Local team wins championship in dramatic finish",
            "Star player signs record-breaking contract",
            "Olympic games preparations underway",
            "Underdog team pulls off major upset",
        ],
        "business": [
            "Stock market reaches new all-time high",
            "Major merger announced between industry leaders",
            "Startup raises $100M in Series B funding",
            "Economic indicators show strong growth",
        ],
    }
    
    topic_lower = topic.lower()
    matching_headlines = []
    
    # Find headlines matching the topic
    for category, headlines in headlines_db.items():
        if topic_lower in category or category in topic_lower:
            matching_headlines = headlines
            break
    
    if not matching_headlines:
        # Default to random headlines if no match
        matching_headlines = headlines_db["technology"]
    
    # Return requested number of headlines
    selected = random.sample(matching_headlines, min(num_headlines, len(matching_headlines)))
    result = f"Top {len(selected)} headlines for '{topic}':\n"
    for i, headline in enumerate(selected, 1):
        result += f"{i}. {headline}\n"
    
    return result


# ============================================================================
# CALCULATION AND PROCESSING TOOLS
# ============================================================================

def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> str:
    """Calculates tip and total bill amount.
    
    Args:
        bill_amount: The original bill amount in dollars
        tip_percentage: The tip percentage (default: 15.0)
        
    Returns:
        A formatted string with tip and total amounts.
        
    STUDENT EXERCISE:
    - Add support for splitting bill among multiple people
    - Include tax calculation
    - Support different currencies
    """
    if bill_amount < 0:
        return "Error: Bill amount cannot be negative."
    
    if tip_percentage < 0 or tip_percentage > 100:
        return "Error: Tip percentage must be between 0 and 100."
    
    tip_amount = bill_amount * (tip_percentage / 100)
    total_amount = bill_amount + tip_amount
    
    return (
        f"Bill Amount: ${bill_amount:.2f}\n"
        f"Tip ({tip_percentage}%): ${tip_amount:.2f}\n"
        f"Total: ${total_amount:.2f}"
    )


def convert_temperature(value: float, from_unit: Literal["C", "F", "K"], to_unit: Literal["C", "F", "K"]) -> str:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin.
    
    Args:
        value: The temperature value to convert
        from_unit: The source unit ('C', 'F', or 'K')
        to_unit: The target unit ('C', 'F', or 'K')
        
    Returns:
        A string with the converted temperature.
        
    STUDENT EXERCISE:
    - Add validation for absolute zero
    - Support batch conversion of multiple temperatures
    - Add descriptive labels (e.g., "freezing", "boiling")
    """
    # Convert to Celsius first
    if from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    else:  # Already Celsius
        celsius = value
    
    # Convert from Celsius to target unit
    if to_unit == "F":
        result = celsius * 9/5 + 32
    elif to_unit == "K":
        result = celsius + 273.15
    else:  # Stay in Celsius
        result = celsius
    
    return f"{value}°{from_unit} = {result:.2f}°{to_unit}"


# ============================================================================
# TEXT PROCESSING TOOLS
# ============================================================================

def analyze_text(text: str) -> str:
    """Analyzes text and returns basic statistics.
    
    Args:
        text: The text to analyze
        
    Returns:
        A formatted string with text statistics.
        
    STUDENT EXERCISE:
    - Add sentiment analysis
    - Count unique words
    - Identify most common words
    - Calculate reading time estimate
    """
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    characters = len(text)
    characters_no_spaces = len(text.replace(' ', ''))
    
    avg_word_length = characters_no_spaces / len(words) if words else 0
    
    return (
        f"Text Analysis:\n"
        f"- Characters: {characters} (including spaces)\n"
        f"- Characters: {characters_no_spaces} (excluding spaces)\n"
        f"- Words: {len(words)}\n"
        f"- Sentences: {sentences}\n"
        f"- Average word length: {avg_word_length:.1f} characters"
    )


# ============================================================================
# DECISION-MAKING TOOLS
# ============================================================================

def make_recommendation(category: str, preferences: str = "") -> str:
    """Makes a recommendation based on category and preferences.
    
    Args:
        category: The category for recommendation (e.g., 'movie', 'restaurant', 'book')
        preferences: Optional user preferences or constraints
        
    Returns:
        A recommendation with reasoning.
        
    STUDENT EXERCISE:
    - Add user rating/review data
    - Implement collaborative filtering
    - Add multiple recommendations with ranking
    - Include price range information
    """
    recommendations = {
        "movie": [
            ("The Shawshank Redemption", "A timeless classic about hope and friendship"),
            ("Inception", "Mind-bending sci-fi thriller"),
            ("Parasite", "Award-winning social commentary"),
        ],
        "restaurant": [
            ("The Italian Corner", "Authentic pasta and cozy atmosphere"),
            ("Sushi Master", "Fresh sushi and modern ambiance"),
            ("Green Leaf", "Healthy vegetarian options"),
        ],
        "book": [
            ("Project Hail Mary", "Exciting sci-fi adventure"),
            ("Atomic Habits", "Practical guide to building good habits"),
            ("The Midnight Library", "Thought-provoking fiction"),
        ],
    }
    
    category_lower = category.lower()
    if category_lower in recommendations:
        name, description = random.choice(recommendations[category_lower])
        result = f"I recommend: {name}\n{description}"
        if preferences:
            result += f"\n\nBased on your preferences: {preferences}"
        return result
    else:
        return f"Sorry, I don't have recommendations for '{category}'. Try 'movie', 'restaurant', or 'book'."


# ============================================================================
# STATEFUL TOOLS (using ToolContext)
# ============================================================================

def add_to_shopping_list(item: str, quantity: int = 1) -> str:
    """Adds an item to a shopping list stored in session state.
    
    This demonstrates how to use session state to maintain data across tool calls.
    
    Args:
        item: The item to add to the shopping list
        quantity: The quantity of the item (default: 1)
        
    Returns:
        Confirmation message with current shopping list.
        
    STUDENT EXERCISE:
    - Add remove_from_shopping_list tool
    - Add clear_shopping_list tool
    - Add categories to items
    - Calculate estimated total cost
    
    NOTE: To use session state, you need to access it via ToolContext.
    This is a simplified example - see ADK documentation for full ToolContext usage.
    """
    # In a real implementation, you would access session.state via ToolContext
    # For this example, we'll just return a message
    return (
        f"Added {quantity}x {item} to your shopping list.\n"
        f"(Note: This is a demo. In a real agent, this would persist in session.state)"
    )
