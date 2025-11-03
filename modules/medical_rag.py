# modules/medical_rag.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

KB_DOCS = [
    {"id": "doc1", "text": "Fever is a body temperature above 100.4°F (38°C).", "source": "CDC"},
    {"id": "doc2", "text": "Minor ankle sprains: RICE – Rest, Ice, Compression, Elevation.", "source": "Ortho_FAQ"},
    {"id": "doc3", "text": "Prescription refills require 24-48 hours for processing.", "source": "Pharmacy_Policy"},
    {"id": "doc4", "text": "Chest pain with shortness of breath can indicate a heart emergency.", "source": "Cardiology_Ref"},
]

embed_model = SentenceTransformer("all-MiniLM-L12-v2")
kb_texts = [d["text"] for d in KB_DOCS]
kb_embeddings = embed_model.encode(kb_texts, convert_to_numpy=True)
d = kb_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(kb_embeddings)

def retrieve_docs(query, top_k=3):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, top_k)
    results = []
    for idx in I[0]:
        if idx < len(KB_DOCS):
            results.append(KB_DOCS[idx])
            break
    return results
