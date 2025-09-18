# Handling Missing Tools in Agentic AI

Agentic AI relies on **LLMs + reasoning + tools + memory**.  
But what happens when the LLM suggests a tool that doesn’t exist?

---

## 🔹 Problem
An LLM may hallucinate a tool (e.g., `flight_search_api`) that is not registered in the framework.

If unchecked, this can:
- Cause errors
- Lead to confusing outputs
- Break the workflow

---

## 🔹 Solution
Agent frameworks (LangChain, LangGraph, CrewAI, etc.) implement **guardrails**:

1. **Validation** – Check the tool name against a registry.
2. **Feedback** – If tool not found, tell the LLM:  
   *“Available tools are: weather_api, calculator.”*
3. **Replanning** – The LLM replans using valid tools or falls back to internal knowledge.
4. **Fallback** – If no tool is suitable, the agent replies based on its own reasoning.

---

## 🔹 Example with LangChain

Below is a Python demo where the agent has only two tools:  
- `weather_api`  
- `calculator`

If the user asks for a missing tool (`flight_search_api`), the framework handles it gracefully.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# Define available tools
def weather_api(location: str) -> str:
    return f"The weather in {location} is sunny (dummy data)."

def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Error in calculation."

tools = [
    Tool(
        name="weather_api",
        func=weather_api,
        description="Get the weather for a given location"
    ),
    Tool(
        name="calculator",
        func=calculator,
        description="Evaluate mathematical expressions"
    ),
]

# Initialize LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Memory (to keep track of interactions)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create an agent with only the tools above
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# --- Example Queries ---
# This one should work (weather_api exists)
print(agent.run("What is the weather in Rome?"))

# This one will fail at first (no flight_search_api tool is registered)
print(agent.run("Book me a flight to Rome using flight_search_api."))
```