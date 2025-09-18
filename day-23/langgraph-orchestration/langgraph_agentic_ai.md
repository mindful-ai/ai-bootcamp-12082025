# LangGraph and Agentic AI

## 🔹 What is LangGraph?

LangGraph is an **open-source framework** built on top of LangChain that
allows developers to **design, visualize, and execute complex
multi-agent workflows** using **graph-based state machines**.\
It is especially useful for creating **Agentic AI solutions**, where
multiple AI agents (or tools) must coordinate to solve tasks.

### Key Features

-   **Graph-based orchestration** of LLM workflows
-   **State management** to allow agents to share knowledge
-   **Branching, loops, and conditions** for dynamic control flow
-   **Multi-agent collaboration**
-   **Visualization of workflows**

------------------------------------------------------------------------

## 🔹 Why is LangGraph Helpful for Agentic AI?

-   **Composable workflows** (agents as nodes, connected by edges)
-   **Branching logic** for flexible task execution
-   **Multi-agent collaboration** with shared memory
-   **Error handling and retries**
-   **Visualization for debugging and design**

------------------------------------------------------------------------

## 🔹 Mini Example: Researcher + Summarizer with Loop

``` python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict

# ---- Shared State ----
class AgentState(TypedDict):
    query: str
    research: str
    summary: str

# ---- Agents ----
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def researcher(state: AgentState):
    result = llm.invoke(f"Research this: {state['query']}")
    return {"research": result.content}

def summarizer(state: AgentState):
    result = llm.invoke(f"Summarize this in 3 sentences: {state['research']}")
    return {"summary": result.content}

def check_summary(state: AgentState):
    if len(state["summary"].split()) > 40:
        return "retry"
    return "ok"

# ---- Workflow ----
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher)
workflow.add_node("summarizer", summarizer)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "summarizer")

workflow.add_conditional_edges(
    "summarizer", check_summary, {"retry": "summarizer", "ok": END}
)

app = workflow.compile()

# Run
final_state = app.invoke({"query": "Latest trends in renewable energy 2025"})
print("Summary:", final_state["summary"])
```

------------------------------------------------------------------------

## 🔹 Multi-Agent Collaboration Example (Planner → Researcher → Summarizer → Critic)

``` python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    subtasks: List[str]
    research: List[str]
    summary: str
    feedback: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def planner(state: AgentState):
    result = llm.invoke(f"Break this task into 3 subtasks: {state['query']}")
    subtasks = [s.strip() for s in result.content.split("\n") if s.strip()]
    return {"subtasks": subtasks, "research": []}

def researcher(state: AgentState):
    for subtask in state["subtasks"]:
        if subtask not in [r.split(":")[0] for r in state["research"]]:
            result = llm.invoke(f"Research this: {subtask}")
            state["research"].append(f"{subtask}: {result.content}")
            return {"research": state["research"]}
    return {"research": state["research"]}

def summarizer(state: AgentState):
    notes = "\n".join(state["research"])
    result = llm.invoke(f"Summarize this research in 5 sentences:\n{notes}")
    return {"summary": result.content}

def critic(state: AgentState):
    result = llm.invoke(
        f"Evaluate this summary. Answer 'approve' or 'revise'.\n{state['summary']}"
    )
    return {"feedback": result.content.lower()}

def check_feedback(state: AgentState):
    if "revise" in state["feedback"]:
        return "revise"
    return "approve"

workflow = StateGraph(AgentState)
workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("summarizer", summarizer)
workflow.add_node("critic", critic)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "summarizer")
workflow.add_edge("summarizer", "critic")

workflow.add_conditional_edges(
    "critic", check_feedback, {"revise": "summarizer", "approve": END}
)

app = workflow.compile()

final_state = app.invoke({"query": "Explain the impact of AI on healthcare in 2025"})
print("Subtasks:", final_state["subtasks"])
print("Summary:", final_state["summary"])
print("Feedback:", final_state["feedback"])
```

------------------------------------------------------------------------

## 🔹 Graph Visualization

``` python
graph = app.get_graph()
graph.draw_png("workflow.png")
```

This will produce a graph like:

    [planner] → [researcher] → [summarizer] → [critic]
                                        ▲          │
                                        └──────────┘

------------------------------------------------------------------------

# 📝 Assessment Problem Statement (Theme 1: Research Assistant)

### Problem

Build a **multi-agent Research Assistant** with LangGraph.\
- Planner: split task into subtasks\
- Researcher: gather info per subtask\
- Summarizer: draft summary\
- Critic: approve or send back for revision

### Deliverables

-   Python code\
-   Graph visualization\
-   Run outputs (subtasks, research, summary, feedback)

------------------------------------------------------------------------

# 📝 Assessment Problem Statement (Theme 2: Travel Planning Assistant)

### Problem

Build an **AI-powered Travel Planning Assistant** with LangGraph.\
- Planner: break trip into day-wise activities\
- Organizer: add details (locations, timings, recommendations)\
- Summarizer: create a short itinerary summary\
- Critic: approve or send back for revision

### Deliverables

-   Python code\
-   Graph visualization\
-   Run outputs (plan, details, summary, feedback)

------------------------------------------------------------------------

# ✅ Evaluation Criteria

-   Correctness\
-   Multi-agent collaboration\
-   Feedback loop handling\
-   Clarity of final output\
-   Graph visualization matches workflow
