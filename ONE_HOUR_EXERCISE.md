# 1-Hour Hands-On Exercise: Your First AI Agent

> **Time**: 60 minutes  
> **Level**: Beginner - No prior agent experience needed  
> **What you'll do**: Modify an agent's behavior and add a custom tool

---

## 🎯 Learning Goals

By the end of this exercise, you will:
- Understand how agent instructions (prompts) control behavior
- Write a custom tool function that an agent can use
- Test and debug agent behavior

---

## ⏱️ Timeline

- **0-10 min**: Setup and run the basic agent
- **10-30 min**: Part 1 - Modify the agent's prompt
- **30-55 min**: Part 2 - Write a custom data analysis tool
- **55-60 min**: Test and reflect

---

## 🚀 Setup (10 minutes)

### Step 1: Install and Run

```bash
# Navigate to the project directory
cd my-first-agent

# Install dependencies
make install

# Run the agent playground
make playground
```

### Step 2: Test the Agent

Once the playground opens in your browser:
1. Try asking: **"What's the weather in London?"**
2. Try asking: **"What time is it in Tokyo?"**
3. Observe how the agent uses tools to answer

### Step 3: Stop the Playground

Press `Ctrl+C` in the terminal to stop the playground. We'll restart it after making changes.

---

## 📝 Part 1: Prompt Engineering (20 minutes)

### What is a Prompt?

The agent's `instruction` is like a job description - it tells the LLM what role to play and how to behave.

### Your Task

Open `app/agent.py` and find the `prompt` variable (around line 69). You'll see something like:

```python
prompt = """
You are a helpful assistant that can provide weather and time information.
Use the available tools to answer user questions accurately.
"""
```

### Exercise 1A: Make it Domain-Specific (10 min)

**Goal**: Transform the agent into a **"Travel Planning Assistant"**

Replace the prompt with:

```python
prompt = """
You are a Travel Planning Assistant specializing in helping people plan trips.

When users ask about a destination:
1. First, check the current weather using get_weather
2. Then, check the local time using get_current_time
3. Provide travel advice based on the weather and time

Always be enthusiastic and helpful. Suggest what to pack based on weather.
Format your responses with clear sections using markdown.
"""
```

**Test it**:
```bash
make playground
```

Ask: **"I'm planning to visit Paris"**

**Observe**: Does the agent behave differently? Does it proactively check weather and time?

### Exercise 1B: Add Constraints (10 min)

**Goal**: Make the agent more concise and structured

Modify the prompt to add this constraint:

```python
prompt = """
You are a Travel Planning Assistant specializing in helping people plan trips.

When users ask about a destination:
1. First, check the current weather using get_weather
2. Then, check the local time using get_current_time
3. Provide travel advice based on the weather and time

IMPORTANT CONSTRAINTS:
- Keep responses under 100 words
- Always use this format:
  **Weather**: [weather info]
  **Local Time**: [time info]
  **Travel Tip**: [one specific tip]
  
- Only provide information if you can get it from tools
- If tools fail, say "Information unavailable" - do NOT make up data
"""
```

**Test it**: Ask the same question again. Is the response more structured?

---

## 🛠️ Part 2: Write a Custom Tool (25 minutes)

### What is a Tool?

A tool is a Python function that gives the agent new capabilities. The agent reads the function's docstring to understand when and how to use it.

### Your Task

Add a data analysis tool that calculates basic statistics.

### Exercise 2A: Write the Function (15 min)

Open `app/custom_tools.py` and add this function at the end:

```python
def calculate_statistics(numbers: list[float]) -> dict:
    """Calculates basic statistical measures for a list of numbers.
    
    Use this tool when the user asks for statistics, averages, or data analysis
    on a set of numbers.
    
    Args:
        numbers: A list of numerical values to analyze
        
    Returns:
        A dictionary containing:
        - mean: The average value
        - median: The middle value
        - min: The smallest value
        - max: The largest value
        - count: How many numbers were analyzed
        
    Example:
        calculate_statistics([1, 2, 3, 4, 5])
        Returns: {"mean": 3.0, "median": 3.0, "min": 1, "max": 5, "count": 5}
    """
    if not numbers:
        return {"error": "No numbers provided"}
    
    sorted_numbers = sorted(numbers)
    n = len(numbers)
    
    # Calculate mean
    mean = sum(numbers) / n
    
    # Calculate median
    if n % 2 == 0:
        median = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        median = sorted_numbers[n//2]
    
    return {
        "mean": round(mean, 2),
        "median": median,
        "min": min(numbers),
        "max": max(numbers),
        "count": n
    }
```

**Key Points**:
- ✅ **Docstring**: Explains what the tool does (the agent reads this!)
- ✅ **Type hints**: `list[float]` and `-> dict` help the agent understand inputs/outputs
- ✅ **Error handling**: Returns an error message if no numbers provided
- ✅ **Clear return format**: Dictionary with labeled values

### Exercise 2B: Add the Tool to Your Agent (5 min)

Open `app/agent.py`:

1. **Import the tool** (add to the imports at the top):
```python
from .custom_tools import calculate_statistics
```

2. **Add it to the tools list** (around line 76):
```python
root_agent = Agent(
    name="root_agent",
    model=ollama_llm,
    instruction=prompt,
    tools=[get_weather, get_current_time, calculate_statistics],  # Add here!
)
```

3. **Update the prompt** to mention the new capability (around line 69):
```python
prompt = """
You are a helpful assistant that can:
- Provide weather information for cities
- Tell the current time in different locations
- Calculate statistics (mean, median, min, max) for lists of numbers

Use the available tools to answer user questions accurately.
When given a list of numbers, use calculate_statistics to analyze them.
"""
```

### Exercise 2C: Test Your Tool (5 min)

```bash
make playground
```

**Test queries**:
1. "What's the average of these numbers: 10, 20, 30, 40, 50?"
2. "Calculate statistics for: 5, 15, 25, 35, 45"
3. "What's the median of 1, 2, 3, 4, 5, 6, 7, 8, 9?"

**Observe**:
- Does the agent call your `calculate_statistics` tool?
- Does it present the results clearly?
- What happens if you give it non-numeric data?

---

## 🤔 Reflection Questions (5 minutes)

Answer these questions (discuss with a partner or write down):

1. **Prompt Engineering**:
   - How did changing the instruction affect the agent's behavior?
   - What happens if your instruction is too vague? Too specific?

2. **Tool Design**:
   - Why is the docstring important for the agent?
   - What would happen if you removed the type hints?
   - How could you improve the `calculate_statistics` tool?

3. **Agent Behavior**:
   - Did the agent always use tools correctly?
   - What happened when you asked ambiguous questions?
   - How would you debug if the agent doesn't use your tool?

---

## 🎓 What You Learned

✅ **Prompt engineering** controls agent behavior without changing code  
✅ **Tools** extend agent capabilities with Python functions  
✅ **Docstrings** are critical - the agent reads them to understand tools  
✅ **Type hints** help the agent use tools correctly  
✅ **Testing** is iterative - refine prompts and tools based on results

---

## 🚀 Optional Challenges (If You Have Extra Time)

### Challenge 1: Add Error Handling
Modify `calculate_statistics` to handle edge cases:
- What if the user passes an empty list?
- What if the list contains non-numeric values?

### Challenge 2: Add More Statistics
Extend the function to also calculate:
- Standard deviation
- Range (max - min)
- Sum of all numbers

### Challenge 3: Create Another Tool
Write a `find_outliers` tool that identifies numbers that are unusually high or low.

Hint: A simple approach is to flag numbers that are more than 2 standard deviations from the mean.

---

## 📚 Next Steps

Want to learn more? Check out:
- **`STUDENT_GUIDE.md`** - Comprehensive exercises and examples
- **`app/agent_parallel.py`** - See how multiple agents work together
- **`app/agent_sequential.py`** - See how to build multi-step pipelines
- **`GEMINI.md`** - Deep technical reference for ADK

---

## 💡 Key Takeaways

> **Agents = LLM + Tools + Instructions**

- The **LLM** provides reasoning and language understanding
- **Tools** provide real capabilities (data access, calculations, APIs)
- **Instructions** guide the LLM's behavior and decision-making

This is fundamentally different from traditional ML where you train a model end-to-end. With agents, you **compose** capabilities and **guide** behavior through instructions.

---

## ✅ Submission (If Required)

Submit the following:
1. Your modified `app/agent.py` file with your custom prompt
2. Your modified `app/custom_tools.py` file with the `calculate_statistics` function
3. A screenshot showing successful use of your custom tool
4. Brief answers to the reflection questions (3-5 sentences each)

**Filename format**: `LastName_FirstName_AgentExercise.zip`

---

Good luck! Remember: **experiment, break things, and learn from errors**. That's how you master agent development! 🤖
