# Create an account here: https://openweathermap.org/api
# https://api.openweathermap.org/data/2.5/weather?q=London&appid=02a9482f1a945b4519e9325d0b7d251d


import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

# ----------- Read OpenAI API key from file -----------
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()  # strip() removes any trailing newlines

# ----------- Set environment variables -----------
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENWEATHERMAP_API_KEY"] = "94d2513070b90c306f61b4a02b3cad38"  # replace with your real key

# ----------- Initialize LLM and tools -----------
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
tools = load_tools(["openweathermap-api"], llm)
weather_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ----------- Streamlit App -----------
def run_weather_app():
    st.title('🌦️ Weather Forecast with LangChain + OpenWeatherMap')
    city = st.text_input('Enter a city name:', '')
    
    if st.button('Get Weather'):
        if city.strip() == "":
            st.warning("⚠️ Please enter a city name.")
        else:
            query = f"What's the weather in {city} in the next 3 hours?"
            report = weather_agent.run(query)
            st.text(report)

# ----------- Main App Run -----------
if __name__ == '__main__':
    run_weather_app()
