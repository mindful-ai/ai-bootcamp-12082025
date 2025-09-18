import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

# ===== LangChain Imports =====
from langchain_openai import OpenAI
from langchain_core.tools import tool
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate


# ==== TOOLS ====

@tool("get_weather", return_direct=True)
def get_weather(city: str) -> str:
    """Get current weather for a given city."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return f"Error fetching weather: {r.text}"
    data = r.json()
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{city}: {desc}, {temp:.1f}°C"


@tool("get_news", return_direct=True)
def get_news(topic: str) -> str:
    """Mock function to fetch top 3 news headlines for a given topic."""
    mock_db = {
        "tech": ["AI adoption in Europe rises", "New smartphone released", "Breakthrough in quantum computing"],
        "sports": ["Local team wins championship", "Star player injured", "Olympics preparation begins"],
    }
    headlines = mock_db.get(topic.lower(), ["General news updates coming soon"])
    return f"Top {topic} news: {', '.join(headlines[:3])}"


@tool("make_briefing", return_direct=True)
def make_briefing(data: str) -> str:
    """Create a short 3–4 sentence morning briefing given combined weather and news data."""
    return f"Good morning! Here’s your personalized briefing:\n{data}\nHave a wonderful day ahead!"


# ==== LLM ====
llm = OpenAI(model="gpt-4o-mini", temperature=0)

# ==== Prompt ====
prompt = PromptTemplate.from_template(
    "You are a morning assistant. You can call tools to fetch weather and news, "
    "then combine them with make_briefing.\n\nUser query: {input}\n"
)

# ==== Agent ====
tools = [get_weather, get_news, make_briefing]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ==== Runner ====
def run(query: str):
    out = agent_executor.invoke({"input": query})
    print("\nFINAL OUTPUT:\n", out["output"])


if __name__ == "__main__":
    run("Give me my morning briefing for London with tech news")
