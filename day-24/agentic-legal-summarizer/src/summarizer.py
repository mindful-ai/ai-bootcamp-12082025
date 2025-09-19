from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI

def make_summarizer(llm_model_name: str = "gpt-4o", temperature: float = 0.0):
    llm = ChatOpenAI(model_name=llm_model_name, temperature=temperature)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain

def summarize_docs(chain, docs):
    return chain.run(docs)
