# src/m2_retriever.py

"""
Milestone 2 – Secure Semantic Retriever
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE

from m2_role_guard import is_access_allowed, get_allowed_roles

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = "chroma_db"
COLLECTION = "company_docs"


def get_collection():
    client = chromadb.PersistentClient(
        path=DB_PATH,
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE
    )
    return client.get_collection(COLLECTION)


def embed_query(query):
    model = SentenceTransformer(MODEL)
    return model.encode([query], convert_to_numpy=True)[0].tolist()


def secure_retrieve(query, role, top_k=5):
    print(f"\n[Query] {query}")
    print(f"[Role] {role}")

    allowed_roles = get_allowed_roles(role)
    print(f"[Allowed Roles] {allowed_roles}")

    col = get_collection()
    q_emb = embed_query(query)

    results = col.query(query_embeddings=[q_emb], n_results=top_k * 2)

    final = []
    for i, meta in enumerate(results["metadatas"][0]):
        if is_access_allowed(role, meta["role"]):
            final.append({
                "chunk_id": results["ids"][0][i],
                "role": meta["role"],
                "source": meta["source_path"],
                "text": results["documents"][0][i]
            })
        if len(final) == top_k:
            break

    if not final:
        print("❌ No authorized documents found")

    return final


if __name__ == "__main__":
    secure_retrieve("quarterly financial report", "Finance")
    secure_retrieve("quarterly financial report", "Marketing")
