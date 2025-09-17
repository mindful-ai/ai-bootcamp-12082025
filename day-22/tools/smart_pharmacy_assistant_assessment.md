# Smart Pharmacy Assistant -- Assessment Problem Statement

## 📝 Title: *"Smart Pharmacy Assistant"*

### Objective

Build a **LangChain-based assistant** to help users with basic
medicine-related queries using tools.

------------------------------------------------------------------------

## Task Description

A local pharmacy wants to set up a **Smart Pharmacy Assistant** that
can:

1.  **Use built-in tools**
    -   Calculator: e.g., compute dosage schedules.\
    -   Python REPL: e.g., convert weight (kg ↔ lbs).
2.  **Custom Tool**
    -   Build a tool called `medicine_info(medicine_name)` that returns
        simple pre-defined information about medicines (e.g., purpose,
        dosage).\

    -   Example dictionary:

        ``` python
        MEDICINE_DB = {
            "paracetamol": "Used for fever and pain. Typical dose: 500mg every 6 hours.",
            "ibuprofen": "Used for inflammation and pain. Typical dose: 400mg every 8 hours.",
            "amoxicillin": "Antibiotic for infections. Typical dose: 500mg every 8 hours."
        }
        ```
3.  **External API (Optional / Bonus)**
    -   Integrate a simple **drug price lookup API** (or mock one with
        dummy values).
4.  **Multi-step execution**
    -   Example: *"Find dosage for paracetamol and calculate total
        tablets needed for 5 days if each tablet is 500mg and the
        patient needs 2 tablets/day."*
5.  **Error Handling**
    -   If a medicine isn't in the database, return: *"Medicine not
        found. Please consult a pharmacist."*

------------------------------------------------------------------------

## Deliverables

1.  **Code Implementation**
    -   Python script or Notebook with tools implemented.\
    -   Show tools working individually before combining into an agent.
2.  **Demonstration Queries**
    -   "Give info about ibuprofen."\
    -   "Convert 70 kg to pounds."\
    -   "If a patient needs 2 paracetamol tablets per day for 7 days,
        how many tablets are required?"\
    -   "What is amoxicillin used for?"\
    -   "Tell me about aspirin" (should trigger error handling).

------------------------------------------------------------------------

## Evaluation Criteria

-   ✅ Proper use of Calculator and Python REPL.\
-   ✅ Working custom tool (`medicine_info`).\
-   ✅ Multi-step chaining between tools.\
-   ✅ Clear handling of unknown inputs.\
-   ✅ Clean, readable, well-documented code.

------------------------------------------------------------------------

## ✅ Outcome

Learners will gain hands-on experience in:\
- Using **LangChain built-in tools**\
- Designing and registering a **custom tool**\
- Performing **multi-step reasoning with chaining**\
- Implementing **error handling**\
- Applying LangChain to a **realistic pharmacy theme**
