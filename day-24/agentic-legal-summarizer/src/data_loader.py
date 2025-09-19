from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

TEXT_CHUNK_SIZE = 1500
TEXT_CHUNK_OVERLAP = 200

def load_documents(folder: str):
    p = Path(folder)
    docs = []
    for f in p.glob("**/*"):
        if f.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(f))
            docs.extend(loader.load())
        elif f.suffix.lower() in {".txt", ".md"}:
            loader = TextLoader(str(f), encoding="utf8")
            docs.extend(loader.load())
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_CHUNK_SIZE,
        chunk_overlap=TEXT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", " "]
    )
    return splitter.split_documents(docs)
