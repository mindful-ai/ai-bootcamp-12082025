# autonomous_based.py
# plan → fetch weather → give packing advice

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# State for the agent
class AgentState(dict):
    pass

# Weather Tool (mock)
def get_weather(city: str):
    return f"In {city}, it will be 15°C with rain tomorrow."

# Node: Decide plan
def planner(state: AgentState):
    query = state["query"]
    if "clothes" in query.lower():
        return {"next": "weather"}
    else:
        return {"next": "llm"}

# Node: Weather lookup
def weather_node(state: AgentState):
    city = "London"  # simple demo
    weather = get_weather(city)
    return {"weather": weather, "next": "llm"}

# Node: LLM reasoning
def llm_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    query = state["query"]
    weather = state.get("weather", "")
    response = llm.invoke(f"User query: {query}\nWeather info: {weather}")
    return {"answer": response.content, "next": END}

# Build LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner)
workflow.add_node("weather", weather_node)
workflow.add_node("llm", llm_node)

workflow.add_edge(START, "planner")
workflow.add_conditional_edges("planner", lambda x: x["next"], {"weather": "weather", "llm": "llm"})
workflow.add_edge("weather", "llm")
workflow.add_edge("llm", END)

graph = workflow.compile()

if __name__ == "__main__":
    print("Autonomous Example:\n")
    response = graph.invoke({"query": "I am visiting London. What clothes should I pack?"})
    print(response["answer"])
