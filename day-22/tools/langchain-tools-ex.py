from langchain.agents import initialize_agent, Tool, load_tools
from langchain.llms import OpenAI
from langchain.utilities import OpenWeatherMapAPIWrapper
import os

# 1. Set up API key

with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()
os.environ["OPENWEATHERMAP_API_KEY"] = "YOUR_API_KEY"

# 2. Initialize LLM
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# 3. Load tools
weather = OpenWeatherMapAPIWrapper()
weather_tool = Tool(
    name="Weather",
    func=weather.run,
    description="Use this tool to get current weather for a city."
)

tools = load_tools(["python_repl", "calculator"], llm=llm)
tools.append(weather_tool)

# 4. Initialize Agent
agent = initialize_agent(
    tools, 
    llm, 
    agent="zero-shot-react-description", 
    verbose=True
)

# 5. Example Queries
print(agent.run("What's the weather in London right now?"))
print(agent.run("If the temperature in Paris is 15 Celsius, convert it to Fahrenheit."))
print(agent.run("If I travel 120 km at 60 km/h, how long will it take?"))
