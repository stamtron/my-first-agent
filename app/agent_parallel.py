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
PARALLEL AGENT ARCHITECTURE - Educational Example

This demonstrates how to use ParallelAgent to run multiple agents concurrently.
Perfect for scenarios where you need multiple perspectives or independent analyses.

USE CASES:
- Research from multiple sources simultaneously
- Getting opinions from different expert personas
- Parallel data processing tasks
- Competitive analysis

STUDENT EXERCISES:
1. Add a third specialist agent (e.g., "health_expert")
2. Modify the synthesizer to compare/contrast the parallel results
3. Add error handling for when one agent fails
4. Experiment with different numbers of parallel agents
"""

import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.apps.app import App
from google.adk.models.lite_llm import LiteLlm

# Import custom tools
from .custom_tools import get_news_headlines, get_stock_price

# Setup Ollama LLM (same as main agent)
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

ollama_llm = LiteLlm(
    model=f"ollama_chat/{OLLAMA_MODEL}",
    api_base=OLLAMA_API_BASE,
    api_key=OLLAMA_API_KEY,
)


# ============================================================================
# STEP 1: Define Specialist Agents
# Each agent has a specific expertise and tools
# ============================================================================

tech_expert = Agent(
    name="tech_expert",
    model=ollama_llm,
    instruction="""
    You are a technology industry expert with deep knowledge of tech companies,
    products, and trends. When asked about a topic, provide insights from a
    technology perspective. Use the available tools to get current information.
    
    Focus on:
    - Technology trends and innovations
    - Tech company analysis
    - Product developments
    - Industry disruptions
    """,
    description="Technology industry expert specializing in tech trends and companies",
    tools=[get_news_headlines, get_stock_price],
    output_key="tech_analysis",  # Saves output to session.state
)

business_expert = Agent(
    name="business_expert", 
    model=ollama_llm,
    instruction="""
    You are a business and finance expert with expertise in markets, economics,
    and corporate strategy. When asked about a topic, provide insights from a
    business and financial perspective. Use the available tools to get current information.
    
    Focus on:
    - Market analysis and trends
    - Financial performance
    - Business strategy
    - Economic implications
    """,
    description="Business and finance expert specializing in markets and strategy",
    tools=[get_news_headlines, get_stock_price],
    output_key="business_analysis",  # Saves output to session.state
)


# ============================================================================
# STEP 2: Create ParallelAgent to Run Specialists Concurrently
# ============================================================================

parallel_experts = ParallelAgent(
    name="parallel_research_team",
    sub_agents=[tech_expert, business_expert],
    description="Runs technology and business experts in parallel for comprehensive analysis",
)


# ============================================================================
# STEP 3: Create Synthesizer Agent to Combine Results
# This agent reads the outputs from the parallel agents (stored in session.state)
# ============================================================================

synthesizer = Agent(
    name="synthesizer",
    model=ollama_llm,
    instruction="""
    You are a synthesis expert who combines multiple perspectives into a coherent analysis.
    
    You will receive two analyses:
    1. Technology Expert Analysis: {tech_analysis}
    2. Business Expert Analysis: {business_analysis}
    
    Your job is to:
    - Identify key insights from each perspective
    - Find common themes and contradictions
    - Provide a balanced, comprehensive summary
    - Highlight unique insights from each expert
    
    Format your response with clear sections:
    ## Key Insights
    ## Common Themes
    ## Different Perspectives
    ## Comprehensive Summary
    """,
    description="Synthesizes multiple expert analyses into a comprehensive report",
    # Note: {tech_analysis} and {business_analysis} are automatically injected from session.state
)


# ============================================================================
# STEP 4: Create Root Agent with Sequential Flow
# User → Parallel Experts → Synthesizer → User
# ============================================================================

root_agent_parallel = Agent(
    name="multi_perspective_analyst",
    model=ollama_llm,
    instruction="""
    You are a research coordinator that provides comprehensive analysis by consulting
    multiple experts in parallel.
    
    When a user asks a question:
    1. Delegate to 'parallel_research_team' to get both tech and business perspectives simultaneously
    2. Then delegate to 'synthesizer' to combine the insights
    3. Present the final synthesized analysis to the user
    
    Always explain that you're consulting multiple experts for a comprehensive view.
    """,
    description="Coordinates parallel expert consultation for comprehensive analysis",
    sub_agents=[parallel_experts, synthesizer],
)


# ============================================================================
# STEP 5: Wrap in App for Production Use
# ============================================================================

app = App(
    root_agent=root_agent_parallel,
    name="app"
)


# ============================================================================
# TESTING INSTRUCTIONS FOR STUDENTS
# ============================================================================
"""
To test this parallel agent architecture:

1. Update your .env file with Ollama configuration
2. Run the agent using:
   
   From project root:
   $ export ROOT_AGENT_MODULE=app.agent_parallel
   $ make playground

3. Try these example queries:
   - "What's happening with Apple?"
   - "Analyze the current state of AI technology"
   - "Tell me about recent business trends"

4. Observe how:
   - Both experts run simultaneously (check timing)
   - Each expert provides their unique perspective
   - The synthesizer combines both viewpoints
   - The final output is more comprehensive than a single agent

DEBUGGING TIPS:
- Check session.state to see intermediate outputs (tech_analysis, business_analysis)
- Add print statements in tools to see execution order
- Use adk's built-in tracing to visualize parallel execution
- Try commenting out one expert to see the difference

EXTENSION IDEAS:
- Add a third expert (e.g., social impact analyst)
- Make the synthesizer compare confidence levels
- Add a fact-checker agent that runs in parallel
- Implement voting/consensus mechanism for conflicting views
"""
