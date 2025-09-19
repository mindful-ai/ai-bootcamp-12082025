from data_loader import load_documents, chunk_documents

def test_chunking():
    docs = load_documents("data")
    chunks = chunk_documents(docs)
    assert len(chunks) > 0
