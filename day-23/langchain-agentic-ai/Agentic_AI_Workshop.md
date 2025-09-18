# Workshop on Agentic AI -- Foundations 

## 1. Definition of Agentic AI

-   **Agentic AI** refers to **AI systems that act as autonomous
    decision-making entities**, capable of perceiving their environment,
    reasoning, planning, and executing actions toward goals.\
-   It goes beyond simple LLMs (which mostly generate text) by adding:
    -   **Agency** (ability to take actions, not just respond)\
    -   **Memory** (short-term & long-term context)\
    -   **Tools/Environment interaction** (APIs, databases, browsers,
        external systems)\
    -   **Goal-driven behavior** (can plan and execute steps toward an
        objective)

📌 In simple terms:\
- An LLM (like GPT) **answers questions**.\
- An Agentic AI **figures out what needs to be done, plans steps, uses
tools, and acts until the goal is achieved**.

------------------------------------------------------------------------

## 2. Relation and Difference: Agentic AI vs. Agents in AI

  --------------------------------------------------------------------------
  **Aspect**        **Traditional AI Agents**           **Agentic AI**
  ----------------- ----------------------------------- --------------------
  **Definition**    AI programs built to sense, reason, LLM-powered
                    and act in an environment (common   autonomous systems
                    in robotics, game AI, RL).          with reasoning,
                                                        planning, tool use,
                                                        and memory.

  **Core            Reinforcement learning, rule-based  LLMs (like GPT),
  Techniques**      planning, state machines.           prompt engineering,
                                                        tool APIs, memory
                                                        frameworks, planning
                                                        algorithms.

  **Environment**   Often physical (robots, sensors) or Mostly digital
                    simulation (games).                 (APIs, knowledge
                                                        bases, workflows),
                                                        though can extend to
                                                        robotics.

  **Scope**         Predefined environments with        Open-ended tasks:
                    limited autonomy.                   research assistant,
                                                        financial analysis,
                                                        customer support,
                                                        automation.

  **Relation**      Agentic AI can be seen as a         
                    **modern extension** of AI agents,  
                    enhanced with natural language      
                    reasoning and the ability to        
                    orchestrate multiple steps          
                    flexibly.                           
  --------------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Quick Starter Example -- Weather to Clothing Agent

### Problem:

"Find the current weather in London and write a short recommendation on
what to wear."

### Traditional LLM (Non-Agentic):

-   If asked directly, it may **guess** the weather based on training
    data (outdated).\
-   No ability to fetch real-time info.

### Agentic AI Flow:

1.  **User goal:** "What should I wear in London today?"\
2.  **Agent Reasoning:**
    -   Step 1: Get real-time weather data.\
    -   Step 2: Interpret weather.\
    -   Step 3: Give clothing suggestion.\
3.  **Agent Tools Used:**
    -   Weather API (fetch live data).\
    -   Reasoning module (LLM).\
    -   Memory (log steps & results).\
4.  **Final Output:**\
    "The weather in London is 14°C with light rain. You should wear a
    waterproof jacket and carry an umbrella."

------------------------------------------------------------------------

## 4. LangChain Implementation -- Weather Agent

### Key Components

-   **Tool**: `get_current_weather(city)` --- calls OpenWeatherMap API\
-   **LLM**: OpenAI model via LangChain wrapper\
-   **Agent**: ReAct agent that decides to call the weather tool and
    then generates advice

(See Python script example `agent_weather.py` from discussion above.)

------------------------------------------------------------------------

## 5. Extended Example -- Travel Activity Planner Agent

### Problem:

"I am visiting Paris for 3 days. I like museums and food experiences.
Please suggest an itinerary with weather-based clothing advice."

### Features:

-   Weather tool\
-   Search tool (mock attractions)\
-   Clothing advice tool\
-   Memory to remember user preferences

### Flow:

1.  User says they like museums and food → stored in memory.\
2.  User asks for Paris itinerary.\
3.  Agent calls attractions + weather tools.\
4.  Agent calls clothing advice.\
5.  Final personalized itinerary with clothing tips.

(See Python script example `agent_travel.py` from discussion above.)

------------------------------------------------------------------------

## 6. Assessment Problem Statement

### Title:

**Build a News & Weather Assistant Agent with LangChain**

### Objective:

Design an **Agentic AI system** using the LangChain ecosystem that can:\
1. Fetch live weather for a city.\
2. Fetch latest headlines for a topic.\
3. Combine both into a personalized morning briefing.

### Requirements:

-   At least two tools: `get_weather`, `get_news`\
-   Rule-based personalization tool: `make_briefing`\
-   Output should be a **3--4 sentence morning briefing**

### Example Input:

"Give me my morning briefing for London with tech news."

### Example Output:

"The weather in London today is 16°C with light showers. You should
carry an umbrella. Here are the top tech news headlines: 'AI adoption in
Europe rises', 'New smartphone released'. Have a great day ahead!"

------------------------------------------------------------------------

## 7. Assessment Solution

(See Python script example `agent_news_weather.py` from discussion
above, with three tools: `get_weather`, `get_news`, `make_briefing`.)

------------------------------------------------------------------------

## 8. Learning Outcomes

-   Understand multiple tool orchestration in LangChain.\
-   Use deterministic + LLM-driven functions together.\
-   Observe agent reasoning trace with `verbose=True`.\
-   Compare plain LLM vs. agentic system.

------------------------------------------------------------------------
