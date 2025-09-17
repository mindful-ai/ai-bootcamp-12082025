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