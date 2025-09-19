from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
# Load API key from file
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()
os.environ["OPENAI_API_KEY"] = openai_api_key

def build_or_load_index(docs, persist=True):
    emb = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = Chroma.from_documents(docs, emb, persist_directory=CHROMA_DIR)
    if persist:
        vectordb.persist()
    return vectordb

def get_retriever(vectordb, k=5):
    return vectordb.as_retriever(search_kwargs={"k": k})
