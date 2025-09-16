# 🌍 LangChain Tools & Travel Assistant Workshop

## 🔹 What are **Tools** in LangChain?

In LangChain, a **Tool** is basically a wrapper around a function (or
API, or database, or service) that an LLM can call when it needs
**external knowledge or actions**.

Think of an LLM as a brain that can **reason and plan**, but it cannot
directly:\
- Search Google\
- Fetch data from a database\
- Do calculations\
- Call APIs

👉 That's where **Tools** come in. They allow the LLM to **interact with
the outside world**.

------------------------------------------------------------------------

## 🔹 Components of a Tool

A LangChain **Tool** usually has:

1.  **Name** -- identifier (e.g., `"calculator"`)\
2.  **Description** -- what the tool does (used for reasoning when the
    LLM picks which tool to call)\
3.  **Function** -- the actual callable Python function (or API call, DB
    query, etc.)

------------------------------------------------------------------------

## 🔹 Workflow with Tools

1.  User gives a query → LLM decides if it needs a tool.\
2.  LLM selects a tool (based on descriptions).\
3.  The tool executes → returns result.\
4.  LLM integrates result into its reasoning and answers.

This process is often managed using **Agents** in LangChain.

------------------------------------------------------------------------

## 🔹 Example: Weather & Math Tool Agent (Intermediate Level)

``` python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import requests

# 1. Define a custom Weather Tool
def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Could not fetch weather."

weather_tool = Tool(
    name="WeatherTool",
    func=get_weather,
    description="Use this tool to get the current weather of a city. Input should be the city name."
)

# 2. Calculator Tool
def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Error in calculation."

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Use this tool to solve math expressions like '23*7' or '100/4'."
)

# 3. Create an LLM + Agent with tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = initialize_agent(
    tools=[weather_tool, calculator_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# 4. Try queries
print(agent.run("What's the weather in Bangalore?"))
print(agent.run("What is 25 * 12 divided by 3?"))
print(agent.run("What's the weather in Mumbai plus the result of 50*2?"))
```

------------------------------------------------------------------------

## 🌍 Project Statement: Travel Assistant with LangChain

We want to build an **AI-powered Travel Assistant** that can:\
1. **Fetch live weather** information for a given city.\
2. **Convert currency** (e.g., USD → INR).\
3. **Look up travel info** (history, tourist spots) from Wikipedia.\
4. **Perform quick calculations**.

The assistant should reason about the query, decide which tool(s) to
use, and return a **natural language answer**.

------------------------------------------------------------------------

## 🔧 Travel Assistant Code (Terminal version)

``` python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import requests
import wikipedia

# Weather Tool
def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "Weather service unavailable."
    except Exception as e:
        return f"Error: {str(e)}"

weather_tool = Tool(
    name="WeatherTool",
    func=get_weather,
    description="Get the current weather of a city."
)

# Currency Converter Tool
def convert_currency(query: str) -> str:
    try:
        amount, from_currency, _, to_currency = query.split()
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url).json()
        result = response.get("result", None)
        if result:
            return f"{amount} {from_currency} = {result:.2f} {to_currency}"
        return "Conversion failed."
    except Exception as e:
        return f"Error: {str(e)}"

currency_tool = Tool(
    name="CurrencyConverter",
    func=convert_currency,
    description="Convert currency. Example: '100 USD to INR'"
)

# Wikipedia Tool
def wiki_search(query: str) -> str:
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return "No Wikipedia information found."

wiki_tool = Tool(
    name="WikipediaSearch",
    func=wiki_search,
    description="Get a short summary of a place or travel-related information."
)

# Calculator Tool
def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Calculation error."

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Solve math expressions like '250*3/7'."
)

# LLM + Agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools=[weather_tool, currency_tool, wiki_tool, calculator_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Example Queries
print(agent.run("What is the weather in Paris right now?"))
print(agent.run("Convert 200 USD to EUR"))
print(agent.run("Tell me about the Eiffel Tower"))
print(agent.run("If three hotels in Tokyo cost 120, 150, and 200 USD per night, what is the average?"))
print(agent.run("I am traveling to London. Give me weather, and convert 500 USD to GBP."))
```

------------------------------------------------------------------------

## 🚀 Streamlit Travel Assistant App

We can now build a **Streamlit UI** for the Travel Assistant.

### `travel_assistant_app.py`

``` python
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import requests
import wikipedia

# Define tools here (Weather, Currency, Wiki, Calculator)...

# Create LLM + Agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools=[weather_tool, currency_tool, wiki_tool, calculator_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

# Streamlit UI
st.set_page_config(page_title="🌍 Travel Assistant", page_icon="✈️", layout="wide")
st.title("🌍 Travel Assistant")
st.markdown("Your personal AI-powered travel helper: weather 🌦️ | currency 💱 | info 📖 | math ➗")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

query = st.text_input("💬 Ask me anything about your travel:")
if query:
    with st.spinner("Thinking..."):
        response = agent.run(query)
    st.session_state["messages"].append({"user": query, "assistant": response})

for msg in st.session_state["messages"]:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Assistant:** {msg['assistant']}")
    st.markdown("---")
```

Run with:

``` bash
streamlit run travel_assistant_app.py
```

------------------------------------------------------------------------

# 📝 Workshop Assignment: Travel Assistant with Itinerary Planner

## Problem Statement

You are tasked with enhancing the **Travel Assistant app** built with
LangChain and Streamlit.

Currently, the assistant can:\
- Fetch live weather 🌦️\
- Convert currencies 💱\
- Provide travel-related summaries from Wikipedia 📖\
- Perform quick calculations ➗

Your goal is to **extend the Travel Assistant with a new tool**:\
- **Itinerary Planner Tool** -- The user should be able to ask queries
like *"Plan a 3-day trip to Paris"*.\
- The tool should:\
- Take **city** and **number of days** as input.\
- Generate a **day-by-day itinerary** including top attractions,
cultural spots, and local experiences.\
- Use Wikipedia summaries (where available).\
- Return results in a **structured and readable format**.

------------------------------------------------------------------------

## ✅ Solution: Adding Itinerary Planner

``` python
def plan_itinerary(query: str) -> str:
    try:
        words = query.split()
        days = next((int(w.replace("-day", "")) for w in words if w.isdigit() or "-day" in w), 3)
        city = words[-1]
        
        intro = f"Here’s a suggested {days}-day itinerary for {city}:

"
        itinerary = ""
        for d in range(1, days + 1):
            try:
                info = wikipedia.summary(city, sentences=2)
            except:
                info = f"Explore highlights of {city}."
            itinerary += f"**Day {d}:** Visit famous landmarks, explore local food, and experience culture. {info}

"
        
        return intro + itinerary
    except Exception as e:
        return f"Error planning itinerary: {str(e)}"

itinerary_tool = Tool(
    name="ItineraryPlanner",
    func=plan_itinerary,
    description="Plan a travel itinerary. Example: 'Plan a 3-day trip to Paris'"
)
```

Then, include `itinerary_tool` in the agent's tool list.

------------------------------------------------------------------------

## 🎯 Example Queries

-   `"Plan a 3-day trip to Paris"`\
-   `"Give me a 5-day itinerary for Tokyo"`\
-   `"I want a 2-day trip to Agra"`\
-   `"Plan 4 days in Rome with must-see places"`

------------------------------------------------------------------------

✅ **Learning Outcomes**\
- Understand **custom tool creation** in LangChain.\
- Learn **how to parse queries** (city + days).\
- Use **Wikipedia + LLM reasoning** for dynamic content generation.\
- Integrate into **Streamlit for UI-based deployment**.


-------------------------------------------------------------------------


```python

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import requests
import wikipedia

# ----------------------------
# 1. Define Tools
# ----------------------------

def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "Weather service unavailable."
    except Exception as e:
        return f"Error: {str(e)}"

weather_tool = Tool(
    name="WeatherTool",
    func=get_weather,
    description="Get the current weather of a city. Input must be a city name."
)

def convert_currency(query: str) -> str:
    """
    Example input: '100 USD to INR'
    """
    try:
        amount, from_currency, _, to_currency = query.split()
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url).json()
        result = response.get("result", None)
        if result:
            return f"{amount} {from_currency} = {result:.2f} {to_currency}"
        return "Conversion failed."
    except Exception as e:
        return f"Error: {str(e)}"

currency_tool = Tool(
    name="CurrencyConverter",
    func=convert_currency,
    description="Convert currency. Input format: '100 USD to INR'"
)

def wiki_search(query: str) -> str:
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return "No Wikipedia information found."

wiki_tool = Tool(
    name="WikipediaSearch",
    func=wiki_search,
    description="Get a short summary of a place or travel-related information."
)

def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Calculation error."

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Solve math expressions like '250*3/7'."
)

# ----------------------------
# NEW: Itinerary Planner Tool
# ----------------------------
def plan_itinerary(query: str) -> str:
    """
    Example input: 'Plan a 3-day trip to Paris'
    """
    try:
        # Naive parsing
        words = query.split()
        days = next((int(w.replace("-day", "")) for w in words if w.isdigit() or "-day" in w), 3)
        city = words[-1]  # last word as city (simple parsing)
        
        intro = f"Here’s a suggested {days}-day itinerary for {city}:\n\n"
        itinerary = ""
        for d in range(1, days + 1):
            try:
                info = wikipedia.summary(city, sentences=2)
            except:
                info = f"Explore highlights of {city}."
            itinerary += f"**Day {d}:** Visit famous landmarks, explore local food, and experience culture. {info}\n\n"
        
        return intro + itinerary
    except Exception as e:
        return f"Error planning itinerary: {str(e)}"

itinerary_tool = Tool(
    name="ItineraryPlanner",
    func=plan_itinerary,
    description="Plan a travel itinerary. Input example: 'Plan a 3-day trip to Paris'"
)

# ----------------------------
# 2. LLM + Agent
# ----------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

agent = initialize_agent(
    tools=[weather_tool, currency_tool, wiki_tool, calculator_tool, itinerary_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

# ----------------------------
# 3. Streamlit UI
# ----------------------------
st.set_page_config(page_title="🌍 Travel Assistant", page_icon="✈️", layout="wide")

st.title("🌍 Travel Assistant")
st.markdown("Your AI-powered travel buddy: weather 🌦️ | currency 💱 | info 📖 | math ➗ | itinerary 🗺️")

# Sidebar
st.sidebar.header("⚙️ Settings")
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.5, 0.1)

# Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input box
query = st.text_input("💬 Ask me anything about your travel (e.g., 'Weather in Paris', 'Convert 100 USD to INR', 'Plan a 3-day trip to Tokyo'):")

if query:
    with st.spinner("Thinking..."):
        response = agent.run(query)

    # Save history
    st.session_state["messages"].append({"user": query, "assistant": response})

# Display chat
for msg in st.session_state["messages"]:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Assistant:** {msg['assistant']}")
    st.markdown("---")



```