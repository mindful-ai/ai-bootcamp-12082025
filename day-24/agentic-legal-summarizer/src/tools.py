from embeddings_index import get_retriever
from summarizer import make_summarizer, summarize_docs

class RetrieverTool:
    def __init__(self, vectordb):
        self.retriever = get_retriever(vectordb)

    def __call__(self, query: str, k: int = 5):
        docs = self.retriever.get_relevant_documents(query)
        return [d.page_content for d in docs]

class SummarizerTool:
    def __init__(self, chain):
        self.chain = chain

    def __call__(self, chunks):
        return summarize_docs(self.chain, chunks)

from langchain.chat_models import ChatOpenAI

def make_json_parser(llm_model_name: str = "gpt-4o"):
    llm = ChatOpenAI(model_name=llm_model_name, temperature=0)
    def parser(text: str) -> str:
        prompt = (
            "Given the following legal summary, return a JSON object with keys: "
            "executive_summary, parties, obligations (list), dates (list), risks (list), action_items (list). "
            "Ensure valid JSON only.\n\nText:\n" + text
        )
        resp = llm.invoke([{"role": "user", "content": prompt}])
        return resp.text()
    return parser
