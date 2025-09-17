# curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=94d2513070b90c306f61b4a02b3cad38"

import os
import requests
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType

# Load API keys
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()

openweathermap_api_key = "94d2513070b90c306f61b4a02b3cad38"  

# Define a function to fetch weather
def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {desc} with temperature {temp}°C."
    else:
        return f"Could not retrieve weather for {city}."

# Wrap as a LangChain Tool
weather_tool = Tool(
    name="WeatherAPI",
    func=get_weather,
    description="Use this tool to get the current weather for a city."
)

# Initialize LLM
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# Register custom tool
tools = [weather_tool]

# Create agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Test query
print(agent.run("What's the weather in London?"))
