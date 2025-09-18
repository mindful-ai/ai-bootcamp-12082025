from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()

# ---- Shared State ----
class AgentState(TypedDict):
    query: str
    days: List[str]
    details: List[str]
    summary: str
    feedback: str

# Use OpenAI model (replace with your key/config if needed)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

# ---- Agents ----
def planner(state: AgentState):
    """Planner: Break trip into day-wise activities"""
    result = llm.invoke(f"Plan a {state['query']} into daily activities")
    days = [line.strip() for line in result.content.split("\n") if line.strip()]
    return {"days": days, "details": []}

def organizer(state: AgentState):
    """Organizer: Add details (locations, timings, recommendations)"""
    for day in state["days"]:
        if day not in [d.split(":")[0] for d in state["details"]]:
            result = llm.invoke(f"Add detailed itinerary for: {day}")
            state["details"].append(f"{day}: {result.content}")
            return {"details": state["details"]}
    return {"details": state["details"]}

def summarizer(state: AgentState):
    """Summarizer: Condense itinerary into short summary"""
    notes = "\n".join(state["details"])
    result = llm.invoke(f"Summarize this trip plan in 5 sentences:\n{notes}")
    return {"summary": result.content}

def critic(state: AgentState):
    """Critic: Evaluate summary"""
    result = llm.invoke(
        f"Review this itinerary summary. If it's clear and concise, answer 'approve'. "
        f"If too vague or too detailed, answer 'revise'.\nSummary:\n{state['summary']}"
    )
    return {"feedback": result.content.lower()}

def check_feedback(state: AgentState):
    """Feedback decision"""
    if "revise" in state["feedback"]:
        return "revise"
    return "approve"

# ---- Build Workflow ----
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner)
workflow.add_node("organizer", organizer)
workflow.add_node("summarizer", summarizer)
workflow.add_node("critic", critic)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "organizer")
workflow.add_edge("organizer", "summarizer")
workflow.add_edge("summarizer", "critic")

workflow.add_conditional_edges(
    "critic",
    check_feedback,
    {"revise": "summarizer", "approve": END}
)

# ---- Compile ----
app = workflow.compile()

# ---- Run Example ----
final_state = app.invoke({"query": "3-day trip to Paris focused on art, food, and culture"})

print("\n--- Travel Plan Output ---")
print("\nDay-wise Plan:", final_state["days"])
print("\nDetailed Itinerary Notes:", "\n".join(final_state["details"]))
print("\nFinal Summary:", final_state["summary"])
print("\nCritic Feedback:", final_state["feedback"])
