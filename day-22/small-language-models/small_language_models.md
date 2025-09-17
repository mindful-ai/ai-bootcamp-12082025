# Small Language Models (SLMs)

## 🔹 What are Small Language Models?

Small Language Models (SLMs) are **language models with fewer
parameters** compared to Large Language Models (LLMs).\
- **LLMs** like GPT-4, LLaMA-70B, or Claude-3 have **billions** of
parameters (7B, 13B, 70B, etc.).\
- **SLMs** are **compact models** with typically **\<1B parameters**,
designed for **efficiency, low resource usage, and specific tasks**.

------------------------------------------------------------------------

## 🔹 Key Features of SLMs

1.  **Lightweight & Efficient** -- Can run on laptops, edge devices, or
    mobile phones.\
2.  **Faster Inference** -- Quicker responses compared to LLMs.\
3.  **Domain-Specific Fine-Tuning** -- Easier to fine-tune for niche
    applications.\
4.  **Cost-Effective** -- Training and inference are cheaper than LLMs.\
5.  **Privacy-Friendly** -- Since they can run locally, they reduce
    dependency on cloud APIs.

------------------------------------------------------------------------

## 🔹 Examples of SLMs

-   **DistilBERT** -- A distilled version of BERT (66M parameters).\
-   **MiniLM** -- A compact Transformer model with \< 33M parameters.\
-   **ALBERT** -- Lightweight BERT variant using parameter sharing.\
-   **GPT-2 Small (124M)** -- One of the earliest small transformer
    models.\
-   **Phi-2 (2.7B)** by Microsoft -- A "small but powerful" model
    optimized for reasoning.

------------------------------------------------------------------------

## 🔹 Real-World Application Example

**Use Case:** A customer support assistant for an **e-commerce
website**.

-   **LLM (e.g., GPT-4)**: Great for broad conversation, but heavy and
    expensive.\
-   **SLM (e.g., DistilBERT fine-tuned on product FAQs)**: Can quickly
    and locally answer **frequently asked questions** like:
    -   *"Where is my order?"*\
    -   *"What is your return policy?"*\
    -   *"Do you ship internationally?"*

👉 This works because the **scope is narrow**, and the **answers are
well-defined**.

------------------------------------------------------------------------

## 🔹 Hands-On Activity (Using Hugging Face)

We'll build a **mini Q&A system** using **DistilBERT (a small language
model)**.

### Step 1: Install dependencies

``` bash
pip install transformers torch
```

### Step 2: Load a Small Language Model

``` python
from transformers import pipeline

# Load DistilBERT for Question Answering
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Example context (e.g., an FAQ)
context = """
Our return policy allows customers to return products within 30 days of purchase.
We offer free shipping for orders above $50.
Currently, we ship only within the United States.
"""

# Ask a question
question = "What is the return period?"
answer = qa_pipeline(question=question, context=context)

print("Question:", question)
print("Answer:", answer['answer'])
```

✅ **Expected Output:**

    Question: What is the return period?
    Answer: 30 days

------------------------------------------------------------------------

## 🔹 Suggested Activity for You

1.  Replace the **context** with your own FAQ or knowledge base.\
2.  Ask **different questions** and see how well the SLM answers.\
3.  Compare with a bigger LLM (e.g., GPT-Neo or GPT-3.5) to see
    **accuracy vs speed trade-off**.

👉 This way, you'll **experience the power of SLMs**: fast, lightweight,
and very useful for **domain-specific Q&A applications**.
