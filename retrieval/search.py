# retrieval/search.py
from modules.medical_rag import retrieve_docs
from utils.config import CONFIG

def retrieve_knowledge(query):
    docs = retrieve_docs(query, top_k=CONFIG["RAG_TOP_K"])

    filtered = []
    query_words = set(query.lower().split())
    for d in docs:
        if query_words & set(d["text"].lower().split()):
            filtered.append(d)
    if not filtered:

        return [{"text": "General health guidance from trusted sources like CDC & WHO.", "source": "General"}]
    return filtered