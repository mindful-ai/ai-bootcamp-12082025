# router_based.py
# Router Agent that sends the query either to a Math Tool or a Weather Tool.

from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
import requests

# Define a simple math tool
def math_tool(query: str) -> str:
    try:
        return str(eval(query))  # quick demo, not for production
    except Exception as e:
        return f"Math error: {e}"

# Define a fake weather tool (replace with real API)
def weather_tool(city: str) -> str:
    # For demo purpose, return fixed value
    return f"The weather in {city} tomorrow is 15°C with rain."

tools = [
    Tool(
        name="Calculator",
        func=math_tool,
        description="Useful for solving math expressions like '245*56'."
    ),
    Tool(
        name="Weather",
        func=weather_tool,
        description="Useful for fetching the weather in a given city."
    )
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a router-based agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    verbose=True
)

if __name__ == "__main__":
    print("Router-based Example:\n")
    print(agent.run("What is 245*56?"))
    print(agent.run("What’s the weather in London tomorrow?"))
