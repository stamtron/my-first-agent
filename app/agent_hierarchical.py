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
HIERARCHICAL MULTI-AGENT ARCHITECTURE - Educational Example

This demonstrates a complex multi-level agent hierarchy with:
- Root coordinator agent
- Department-level agents (each with their own sub-agents)
- Specialist agents at the leaf level

This architecture is useful for:
- Complex decision-making systems
- Enterprise-scale applications
- Domain-specific expertise organization
- Modular, maintainable agent systems

STUDENT EXERCISES:
1. Add a new department (e.g., "legal_department")
2. Create cross-department collaboration scenarios
3. Add escalation logic (specialist → department → root)
4. Implement priority/urgency routing
"""

import os
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models.lite_llm import LiteLlm

# Import custom tools
from .custom_tools import (
    get_stock_price,
    get_news_headlines,
    calculate_tip,
    convert_temperature,
    make_recommendation,
    analyze_text,
)

# Setup Ollama LLM
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

ollama_llm = LiteLlm(
    model=f"ollama_chat/{OLLAMA_MODEL}",
    api_base=OLLAMA_API_BASE,
    api_key=OLLAMA_API_KEY,
)


# ============================================================================
# LEVEL 3: Specialist Agents (Leaf Nodes)
# These are the most specialized agents with specific tools and expertise
# ============================================================================

# Finance Department Specialists
stock_analyst = Agent(
    name="stock_analyst",
    model=ollama_llm,
    instruction="""
    You are a stock market analyst specializing in equity analysis and market trends.
    Use the stock price tool to provide current market data and analysis.
    Always provide context and interpretation, not just raw numbers.
    """,
    description="Analyzes stock prices and market trends",
    tools=[get_stock_price, get_news_headlines],
)

financial_news_analyst = Agent(
    name="financial_news_analyst",
    model=ollama_llm,
    instruction="""
    You are a financial news analyst who tracks and interprets business news.
    Focus on how news events impact markets and businesses.
    Provide actionable insights from news headlines.
    """,
    description="Analyzes financial and business news",
    tools=[get_news_headlines],
)

# Customer Service Department Specialists
recommendation_specialist = Agent(
    name="recommendation_specialist",
    model=ollama_llm,
    instruction="""
    You are a recommendation specialist who helps users make decisions.
    Ask clarifying questions if needed, then provide personalized recommendations
    with clear reasoning. Use the recommendation tool for suggestions.
    """,
    description="Provides personalized recommendations",
    tools=[make_recommendation],
)

calculation_assistant = Agent(
    name="calculation_assistant",
    model=ollama_llm,
    instruction="""
    You are a calculation assistant who helps with everyday math problems.
    You can calculate tips, convert temperatures, and perform other useful calculations.
    Always show your work and explain the results clearly.
    """,
    description="Performs calculations and conversions",
    tools=[calculate_tip, convert_temperature],
)

# Research Department Specialists
content_analyst = Agent(
    name="content_analyst",
    model=ollama_llm,
    instruction="""
    You are a content analyst who examines text and provides insights.
    Use the text analysis tool to provide statistics and observations.
    Offer suggestions for improvement when appropriate.
    """,
    description="Analyzes text content and provides insights",
    tools=[analyze_text],
)

news_researcher = Agent(
    name="news_researcher",
    model=ollama_llm,
    instruction="""
    You are a news researcher who finds and summarizes current information.
    Focus on providing comprehensive, well-organized research on topics.
    Cite your sources and provide context.
    """,
    description="Researches current news and information",
    tools=[get_news_headlines],
)


# ============================================================================
# LEVEL 2: Department Agents (Middle Management)
# These agents coordinate specialists within their domain
# ============================================================================

finance_department = Agent(
    name="finance_department",
    model=ollama_llm,
    instruction="""
    You are the Finance Department coordinator. You manage two specialists:
    - stock_analyst: For stock prices and market analysis
    - financial_news_analyst: For business news and financial events
    
    When you receive a finance-related query:
    1. Determine which specialist(s) are needed
    2. Delegate to the appropriate specialist(s)
    3. Synthesize their responses if multiple specialists are used
    4. Provide a comprehensive answer to the user
    
    Handle questions about: stocks, markets, financial news, business trends.
    """,
    description="Coordinates financial analysis and business intelligence",
    sub_agents=[stock_analyst, financial_news_analyst],
)

customer_service_department = Agent(
    name="customer_service_department",
    model=ollama_llm,
    instruction="""
    You are the Customer Service Department coordinator. You manage two specialists:
    - recommendation_specialist: For helping users make decisions
    - calculation_assistant: For tips, conversions, and calculations
    
    When you receive a customer service query:
    1. Understand what the user needs help with
    2. Delegate to the appropriate specialist
    3. Ensure the user gets a friendly, helpful response
    
    Handle questions about: recommendations, calculations, tips, conversions.
    """,
    description="Coordinates customer assistance and practical help",
    sub_agents=[recommendation_specialist, calculation_assistant],
)

research_department = Agent(
    name="research_department",
    model=ollama_llm,
    instruction="""
    You are the Research Department coordinator. You manage two specialists:
    - content_analyst: For analyzing and evaluating text
    - news_researcher: For finding current information on topics
    
    When you receive a research query:
    1. Determine what type of research is needed
    2. Delegate to the appropriate specialist(s)
    3. Organize and present the research findings clearly
    
    Handle questions about: general news, content analysis, research topics.
    """,
    description="Coordinates research and information gathering",
    sub_agents=[content_analyst, news_researcher],
)


# ============================================================================
# LEVEL 1: Root Coordinator Agent (Top Level)
# This agent routes queries to the appropriate department
# ============================================================================

root_agent_hierarchical = Agent(
    name="enterprise_assistant",
    model=ollama_llm,
    instruction="""
    You are an Enterprise Assistant that coordinates three departments:
    
    1. **Finance Department**: Handles stocks, markets, financial news, business trends
    2. **Customer Service Department**: Handles recommendations, calculations, tips, conversions
    3. **Research Department**: Handles general research, news, content analysis
    
    Your workflow:
    1. Greet the user warmly and understand their request
    2. Identify which department(s) should handle the request
    3. Delegate to the appropriate department(s)
    4. Present the department's response to the user
    5. Ask if they need anything else
    
    Routing Guidelines:
    - Stock/market/financial questions → Finance Department
    - Recommendations/calculations/tips → Customer Service Department  
    - General research/news/text analysis → Research Department
    - If unclear, ask the user for clarification
    - For complex queries, you may need to consult multiple departments
    
    Always be professional, helpful, and efficient.
    """,
    description="Enterprise-level assistant coordinating multiple specialized departments",
    sub_agents=[
        finance_department,
        customer_service_department,
        research_department,
    ],
)


# ============================================================================
# Wrap in App
# ============================================================================

app = App(
    root_agent=root_agent_hierarchical,
    name="app"
)


# ============================================================================
# TESTING INSTRUCTIONS FOR STUDENTS
# ============================================================================
"""
To test this hierarchical agent architecture:

1. Run the agent:
   $ export ROOT_AGENT_MODULE=app.agent_hierarchical
   $ make playground
   
   Or:
   $ adk web --agent app.agent_hierarchical:root_agent_hierarchical

2. Try queries that test different levels:

   LEVEL 1 (Root) - Routing:
   - "What can you help me with?"
   - "I need help with multiple things"
   
   LEVEL 2 (Department) - Coordination:
   - "Tell me about Apple stock and recent tech news" (Finance Dept)
   - "I need a movie recommendation and help calculating a tip" (Customer Service)
   - "Research artificial intelligence and analyze this text: [text]" (Research)
   
   LEVEL 3 (Specialist) - Execution:
   - "What's the current price of GOOGL?" (Stock Analyst)
   - "Convert 100°F to Celsius" (Calculation Assistant)
   - "Analyze this text: The quick brown fox..." (Content Analyst)

3. Observe the delegation chain:
   User → Root → Department → Specialist → Department → Root → User

ARCHITECTURE BENEFITS:
✅ Separation of Concerns: Each agent has a clear, focused responsibility
✅ Scalability: Easy to add new departments or specialists
✅ Maintainability: Changes to one specialist don't affect others
✅ Reusability: Specialists can be shared across departments
✅ Clear Routing: Hierarchical structure makes delegation logical

ARCHITECTURE TRADE-OFFS:
⚠️ Latency: More hops = more time (3 levels of delegation)
⚠️ Complexity: More agents = more to manage and debug
⚠️ Cost: More LLM calls = higher API costs
⚠️ Coordination: Requires clear instructions at each level

DEBUGGING TIPS:
1. Test specialists individually first
2. Then test departments with their specialists
3. Finally test the full hierarchy
4. Use logging to trace the delegation path
5. Check session.state at each level

VISUALIZATION:
```
                    [Root: Enterprise Assistant]
                              |
        +---------------------+---------------------+
        |                     |                     |
  [Finance Dept]    [Customer Service]      [Research Dept]
        |                     |                     |
    +---+---+            +----+----+           +----+----+
    |       |            |         |           |         |
[Stock] [News]      [Recommend] [Calc]    [Content] [News]
```

EXTENSION IDEAS:

1. **Add Cross-Department Collaboration**:
   - Create queries that need multiple departments
   - Implement a coordinator that combines department outputs

2. **Add Escalation Logic**:
   - If specialist can't handle → escalate to department
   - If department can't handle → escalate to root
   - Root can then try a different department

3. **Add Priority/Urgency Routing**:
   - High-priority queries go to faster specialists
   - Complex queries get more thorough analysis

4. **Add Caching/Memory**:
   - Remember previous queries from the same user
   - Avoid re-analyzing the same stock multiple times

5. **Add Analytics**:
   - Track which departments are used most
   - Measure response times at each level
   - Identify bottlenecks

6. **Add New Departments**:
   - Legal Department (compliance, regulations)
   - HR Department (policies, benefits)
   - IT Department (technical support)

7. **Implement Load Balancing**:
   - If one specialist is busy, route to another
   - Distribute work across multiple instances

8. **Add Quality Assurance**:
   - QA agent reviews specialist outputs
   - Ensures consistency and accuracy
"""
