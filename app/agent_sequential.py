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
SEQUENTIAL AGENT ARCHITECTURE - Educational Example

This demonstrates how to use SequentialAgent to create a pipeline where agents
execute one after another, with each agent building on the previous agent's work.

USE CASES:
- Data processing pipelines (collect → clean → analyze → report)
- Multi-stage workflows (research → draft → review → finalize)
- Progressive refinement (rough draft → detailed → polished)
- Step-by-step problem solving

STUDENT EXERCISES:
1. Add a fourth stage to the pipeline (e.g., "fact_checker")
2. Make agents skip stages based on conditions
3. Add error recovery (if one stage fails, retry or use fallback)
4. Create a feedback loop (output goes back to earlier stage)
"""

import os
from google.adk.agents import Agent, SequentialAgent
from google.adk.apps.app import App
from google.adk.models.lite_llm import LiteLlm

# Import custom tools
from .custom_tools import get_news_headlines, analyze_text

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
# STEP 1: Define Pipeline Stages
# Each agent performs one specific task in the sequence
# ============================================================================

# Stage 1: Research Collector
research_collector = Agent(
    name="research_collector",
    model=ollama_llm,
    instruction="""
    You are a research collector. Your job is to gather relevant information
    about the user's topic using the available tools.
    
    Steps:
    1. Identify the main topic from the user's question
    2. Use get_news_headlines to find recent information
    3. Summarize the key findings in a clear, organized way
    4. Save your findings for the next stage
    
    Output format:
    ## Research Topic: [topic]
    ## Key Findings:
    - [finding 1]
    - [finding 2]
    - [finding 3]
    """,
    description="Collects research information on a given topic",
    tools=[get_news_headlines],
    output_key="research_findings",  # Next agent will use this
)

# Stage 2: Content Drafter
content_drafter = Agent(
    name="content_drafter",
    model=ollama_llm,
    instruction="""
    You are a content drafter. You receive research findings and create
    a well-structured draft article or report.
    
    Research findings from previous stage:
    {research_findings}
    
    Your tasks:
    1. Organize the research into a logical structure
    2. Write an engaging introduction
    3. Develop main points with supporting details
    4. Add a conclusion
    5. Keep it concise but informative (3-4 paragraphs)
    
    Focus on clarity and readability.
    """,
    description="Drafts content based on research findings",
    output_key="draft_content",  # Next agent will use this
)

# Stage 3: Content Polisher
content_polisher = Agent(
    name="content_polisher",
    model=ollama_llm,
    instruction="""
    You are a content polisher and editor. You receive a draft and improve it.
    
    Draft content from previous stage:
    {draft_content}
    
    Your tasks:
    1. Improve sentence structure and flow
    2. Enhance clarity and conciseness
    3. Add engaging transitions
    4. Ensure professional tone
    5. Fix any grammatical issues
    6. Add a compelling title
    
    Output the polished, final version ready for publication.
    """,
    description="Polishes and refines draft content",
    tools=[analyze_text],  # Can analyze the draft
    output_key="final_content",
)


# ============================================================================
# STEP 2: Create Sequential Pipeline
# Agents execute in order: collector → drafter → polisher
# ============================================================================

content_pipeline = SequentialAgent(
    name="content_creation_pipeline",
    sub_agents=[
        research_collector,
        content_drafter,
        content_polisher,
    ],
    description="Sequential pipeline for research, drafting, and polishing content",
)


# ============================================================================
# STEP 3: Create Root Agent to Manage the Pipeline
# ============================================================================

root_agent_sequential = Agent(
    name="content_creator",
    model=ollama_llm,
    instruction="""
    You are a content creation assistant that produces high-quality articles
    through a multi-stage process.
    
    When a user requests content on a topic:
    1. Acknowledge their request
    2. Delegate to 'content_creation_pipeline' which will:
       - Research the topic
       - Draft the content
       - Polish it to perfection
    3. Present the final polished content to the user
    
    Explain that you're using a professional 3-stage process for quality results.
    """,
    description="Manages content creation through a sequential pipeline",
    sub_agents=[content_pipeline],
)


# ============================================================================
# STEP 4: Wrap in App
# ============================================================================

app = App(
    root_agent=root_agent_sequential,
    name="app"
)


# ============================================================================
# TESTING INSTRUCTIONS FOR STUDENTS
# ============================================================================
"""
To test this sequential agent architecture:

1. Run the agent:
   $ export ROOT_AGENT_MODULE=app.agent_sequential
   $ make playground

2. Try these example queries:
   - "Write an article about artificial intelligence"
   - "Create content about climate change"
   - "I need a piece about space exploration"

3. Observe the sequential flow:
   - Stage 1: Research is collected
   - Stage 2: Draft is created from research
   - Stage 3: Draft is polished into final content
   - Each stage builds on the previous one

4. Check session.state to see intermediate outputs:
   - research_findings (after stage 1)
   - draft_content (after stage 2)
   - final_content (after stage 3)

DEBUGGING TIPS:
- Add logging to see when each agent starts/finishes
- Check the output_key values in session.state
- Try running each agent individually first
- Comment out stages to test partial pipelines

COMPARISON WITH PARALLEL:
- Sequential: One agent waits for previous to finish
- Parallel: All agents run simultaneously
- Sequential is better when: later stages need earlier results
- Parallel is better when: tasks are independent

EXTENSION IDEAS:
1. Add conditional branching:
   - If research is insufficient, loop back to collector
   - If draft is too short, regenerate with more detail

2. Add quality checks:
   - Validator agent between stages
   - Reject and retry if quality is low

3. Add user feedback loop:
   - After draft, ask user for feedback
   - Incorporate feedback in polishing stage

4. Create different pipelines for different content types:
   - Blog post pipeline
   - Technical documentation pipeline
   - Social media content pipeline

5. Add metrics tracking:
   - Time spent in each stage
   - Content length at each stage
   - Quality score progression
"""
