# 📝 Hands-On Assessment: Small Language Models (SLMs)

## Title: Building a Domain-Specific Q&A Bot using a Small Language Model

### Objective

Use a **small language model (e.g., DistilBERT)** to create a **Question
Answering (QA) system** on a **domain-specific dataset** (e.g., FAQ,
company policies, or Wikipedia text).

------------------------------------------------------------------------

## Requirements

1.  Load a small pre-trained model (DistilBERT or MiniLM).\
2.  Provide a custom **context document** (given FAQ, short article, or
    policy text).\
3.  Build a **QA pipeline** where the user can ask natural language
    questions.\
4.  Display the most relevant answer extracted by the SLM.\
5.  (**Bonus**) Extend the system to allow multiple contexts (like
    multiple FAQs or documents).

------------------------------------------------------------------------

## Example Dataset (Context Provided in Workshop)

``` text
Company FAQ:
1. Orders above $100 qualify for free shipping.
2. Products can be returned within 15 days of delivery.
3. Customer support is available 24/7 via email and chat.
4. Currently, we only deliver within India.
```

### Example Questions:

-   "How many days do I have to return a product?"\
-   "Do you ship outside India?"\
-   "When is customer support available?"



------------------------------------------------------------------------

### ✅ Expected Output

    Q: How many days do I have to return a product?
    A: 15 days

    Q: Do you ship outside India?
    A: only deliver within India

    Q: When is customer support available?
    A: 24/7

------------------------------------------------------------------------

## 🔹 Extension (For Advanced Participants)

-   Load **multiple FAQ documents** and build a retrieval system.\
-   Compare results of **SLM (DistilBERT)** vs a **larger model
    (GPT-Neo)**.\
-   Measure **speed difference** between SLM and LLM.

------------------------------------------------------------------------

## Learning Outcomes

-   Understand how to use SLMs for real-world tasks.\
-   Experience the trade-off between **speed** and **accuracy**.\
-   Leave with a **working application** they can adapt to their own use
    cases.
