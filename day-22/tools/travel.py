
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import requests
# import wikipedia


# Load API keys
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()

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

# def wiki_search(query: str) -> str:
#     try:
#         summary = wikipedia.summary(query, sentences=2)
#         return summary
#     except Exception:
#         return "No Wikipedia information found."

# wiki_tool = Tool(
#     name="WikipediaSearch",
#     func=wiki_search,
#     description="Get a short summary of a place or travel-related information."
# )

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
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)

agent = initialize_agent(
    tools=[weather_tool, currency_tool, calculator_tool, itinerary_tool],
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


