# src/m2_retriever.py

"""
Milestone 2 – Phase B2
Secure Role-Based Retriever
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from pathlib import Path

from m2_role_guard import is_access_allowed, get_allowed_roles

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "company_docs"


def load_chroma_collection():
    """
    Load persistent ChromaDB collection.
    """
    settings = Settings()
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=settings,
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE
    )
    return client.get_collection(COLLECTION_NAME)


def embed_query(query: str):
    """
    Generate embedding for user query.
    """
    model = SentenceTransformer(MODEL_NAME)
    embedding = model.encode([query], convert_to_numpy=True)[0]
    return embedding.tolist()


def secure_retrieve(query: str, user_role: str, top_k: int = 5):
    """
    Retrieve documents securely based on user role.
    """
    print(f"\n[Retriever] Query: '{query}'")
    print(f"[Retriever] User Role: {user_role}")

    allowed_roles = get_allowed_roles(user_role)
    print(f"[Retriever] Allowed Roles: {allowed_roles}")

    collection = load_chroma_collection()
    query_embedding = embed_query(query)

    # Retrieve more than needed, then filter
    raw_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k * 2
    )

    secure_results = []

    for i in range(len(raw_results["ids"][0])):
        metadata = raw_results["metadatas"][0][i]
        doc_role = metadata.get("role")

        if is_access_allowed(user_role, doc_role):
            secure_results.append({
                "chunk_id": raw_results["ids"][0][i],
                "role": doc_role,
                "source": metadata.get("source_path"),
                "text": raw_results["documents"][0][i]
            })

        if len(secure_results) >= top_k:
            break

    if not secure_results:
        print("[Retriever] No authorized documents found.")

    return secure_results


def demo():
    print("\n=== Secure Retriever Demo ===")

    tests = [
        ("What is the quarterly financial performance?", "Finance"),
        ("What is the quarterly financial performance?", "Marketing"),
        ("Explain engineering architecture", "Engineering"),
    ]

    for query, role in tests:
        results = secure_retrieve(query, role)
        print(f"\nResults for role '{role}':")
        for r in results:
            print(f"- {r['chunk_id']} ({r['role']}) → {r['source']}")


if __name__ == "__main__":
    demo()
