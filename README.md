# my-first-agent

A hands-on learning repository for building AI agents with Google's Agent Development Kit (ADK).

> **For Students**: This repository is designed for a 1-hour hands-on exercise to learn the basics of AI agents.

---

## 🎯 Getting Started

### **👉 Start Here: [ONE_HOUR_EXERCISE.md](ONE_HOUR_EXERCISE.md)**

This is your main assignment! It will guide you through:
1. Setting up and running your first agent
2. Modifying agent behavior through prompt engineering
3. Writing a custom tool function
4. Testing and debugging

**Time required**: 60 minutes

---

## 📁 Project Structure

```
my-first-agent/
├── app/
│   ├── agent.py              # Main agent - YOU'LL EDIT THIS
│   ├── custom_tools.py       # Tools library - YOU'LL ADD A FUNCTION HERE
│   ├── agent_parallel.py     # Example: Multiple agents working together
│   ├── agent_sequential.py   # Example: Multi-step pipeline
│   └── agent_hierarchical.py # Example: Complex multi-level system
├── ONE_HOUR_EXERCISE.md      # Your assignment (START HERE!)
├── README.md                 # This file
└── pyproject.toml            # Project dependencies
```

---

## ⚙️ Setup Instructions

### Prerequisites

You need these tools installed:
- **uv** (Python package manager) - [Install here](https://docs.astral.sh/uv/getting-started/installation/)
- **make** (build tool) - Pre-installed on Mac/Linux

### Installation

```bash
# 1. Navigate to the project directory
cd my-first-agent

# 2. Install dependencies
make install

# 3. Run the agent playground
make playground
```

The playground will open in your browser at `http://localhost:8080`

---

## 🚀 Quick Commands

| Command | What it does |
|---------|--------------|
| `make install` | Install all dependencies |
| `make playground` | Start the agent in your browser |
| `make test` | Run tests to verify your code works |

**To stop the playground**: Press `Ctrl+C` in the terminal

---

## 🔄 Running Different Agent Examples

After completing the main exercise, you can explore more complex examples:

```bash
# Run the parallel agent example (multiple experts)
export ROOT_AGENT_MODULE=app.agent_parallel
make playground

# Run the sequential pipeline example
export ROOT_AGENT_MODULE=app.agent_sequential
make playground

# Run the hierarchical system example
export ROOT_AGENT_MODULE=app.agent_hierarchical
make playground

# Return to your modified agent
export ROOT_AGENT_MODULE=app.agent
make playground
```

---

## 📚 What You'll Learn

By the end of the exercise, you'll understand:

✅ How AI agents differ from traditional ML models  
✅ How to control agent behavior with prompts (instructions)  
✅ How to give agents new capabilities with custom tools  
✅ How to test and debug agent systems  

---

## ❓ Getting Help

**Having issues?**

1. **Check your setup**: Make sure `make install` completed successfully
2. **Read error messages**: They usually tell you what's wrong
3. **Ask your instructor**: That's what they're here for!

**Common issues**:
- "Module not found" → Make sure you're in the `my-first-agent` directory
- "Port already in use" → Stop the playground with `Ctrl+C` first
- Agent doesn't use your tool → Check the docstring and agent instruction

---

## 🎓 Next Steps

After completing the 1-hour exercise:

1. **Explore the example agents** in the `app/` directory
2. **Read the code comments** - they explain how everything works
3. **Experiment!** Try modifying the examples and see what happens
4. **Build your own agent** for a problem you care about

---

## 📖 Additional Resources

- [ADK Official Documentation](https://github.com/google/adk-python)
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)

---

**Ready to start?** Open [ONE_HOUR_EXERCISE.md](ONE_HOUR_EXERCISE.md) and let's build your first agent! 🤖
