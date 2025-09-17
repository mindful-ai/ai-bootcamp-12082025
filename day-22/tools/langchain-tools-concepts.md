# Smart Travel Assistant with LangChain -- Workshop Manual

This manual demonstrates how to use **LangChain Tools** step by step
with a running example: a **Smart Travel Assistant**.

------------------------------------------------------------------------

## 1. Using Built-in LangChain Tools (Search, Calculator, Python REPL, SerpAPI)

``` python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.tools.python.tool import PythonREPLTool

# Initialize LLM
llm = OpenAI(temperature=0)

# Search tool
search = SerpAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for searching current travel info"
    ),
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="Useful for calculating travel costs"
    ),
    PythonREPLTool(),  # for running python snippets
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Example queries
agent.run("Search for best tourist attractions in Paris")
agent.run("What is 120 euros + 45 euros in INR if 1 Euro = 90 INR?")
agent.run("Use Python to convert 70 Fahrenheit to Celsius")
```

------------------------------------------------------------------------

## 2. Building a Custom Tool

``` python
from langchain.tools import tool

@tool("flight_cost_estimator")
def flight_cost_estimator(data: str) -> str:
    """Estimate flight cost given distance in km and class (economy/business)."""
    try:
        distance, travel_class = data.split(",")
        distance = float(distance.strip())
        base_rate = 0.1 if travel_class.strip() == "economy" else 0.25
        return f"Estimated flight cost: ${distance * base_rate:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"
```

------------------------------------------------------------------------

## 3. Tool Chaining & Multi-step Execution with Output Parsers

``` python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

distance_prompt = PromptTemplate(
    input_variables=["city1", "city2"],
    template="Find the approximate distance in km between {city1} and {city2}."
)

distance_chain = LLMChain(llm=llm, prompt=distance_prompt)

city1, city2 = "Paris", "Rome"
distance = distance_chain.run({"city1": city1, "city2": city2})
print("Distance:", distance)

# Pass to custom tool
print(flight_cost_estimator(f"{distance}, economy"))
```

------------------------------------------------------------------------

## 4. Integrating External APIs (Weather, Finance, etc.)

``` python
import requests
from langchain.tools import tool

@tool("weather_info")
def weather_info(city: str) -> str:
    """Get current weather of a city using OpenWeatherMap API."""
    api_key = "YOUR_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        return f"Weather in {city}: {response['main']['temp']}°C, {response['weather'][0]['description']}"
    return "Weather data not available."
```

------------------------------------------------------------------------

## 5. Managing Tool Inputs and Outputs with Interfaces

``` python
# Example: Normalizing inputs before passing
def normalize_city_input(city: str) -> str:
    return city.strip().title()

print(weather_info(normalize_city_input("  new york ")))
```

------------------------------------------------------------------------

## 6. Error Handling & Tool Failover Strategies

``` python
def safe_tool_call(tool_func, *args, **kwargs):
    try:
        return tool_func(*args, **kwargs)
    except Exception as e:
        return f"Fallback response: Error occurred - {e}"

# Example with failover
print(safe_tool_call(weather_info, "InvalidCity123"))
```

------------------------------------------------------------------------

## 7. Creating & Registering Tools for Reusability in Agents

``` python
# Register reusable tools
tools.extend([
    flight_cost_estimator,
    weather_info
])

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now use them inside agent
agent.run("What is the weather in Paris and estimate flight cost from Paris to Rome in business class")
```

------------------------------------------------------------------------

## 🔑 Notes

-   Replace `"YOUR_API_KEY"` with your OpenWeatherMap API key.
-   You can use `WikipediaAPIWrapper` instead of installing the
    `wikipedia` library.
-   Tools can be reused, chained, and registered for building powerful
    assistants.

------------------------------------------------------------------------

## ✅ Outcome

With this **single Travel Assistant demo**, you can illustrate:

-   Using LangChain's built-in tools\
-   Creating custom tools\
-   Tool chaining and parsing\
-   Integrating real APIs\
-   Handling inputs/outputs cleanly\
-   Error handling & fallback strategies\
-   Reusable tool registration
