from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import ChatOpenAI
from tools import RetrieverTool, SummarizerTool, make_json_parser
from embeddings_index import build_or_load_index
from data_loader import load_documents, chunk_documents
from summarizer import make_summarizer
import os

# Load API key from file
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()
os.environ["OPENAI_API_KEY"] = openai_api_key

def bootstrap(db_dir: str = "./chroma_db", docs_folder: str = "./data"):
    docs = load_documents(docs_folder)
    chunks = chunk_documents(docs)
    vectordb = build_or_load_index(chunks, persist=True)
    retriever_tool = RetrieverTool(vectordb)
    summarizer_chain = make_summarizer()
    summarizer_tool = SummarizerTool(summarizer_chain)
    json_parser = make_json_parser()
    memory = MemorySaver()
    model = ChatOpenAI(model_name="gpt-4o", temperature=0.0, api_key=openai_api_key)
    tools = [retriever_tool, summarizer_tool, json_parser]
    agent = create_react_agent(model=model, tools=tools, checkpointer=memory)
    return agent

if __name__ == "__main__":
    a = bootstrap()
    rv = a.invoke({"messages": [{"role": "user", "content": "Summarize the attached contract and extract action items."}]})
    print(rv)
