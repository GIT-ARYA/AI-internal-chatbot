# src/m2_embedding_validation.py

"""
Milestone 2 – Module 3
Embedding Generation & Validation
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

CSV_PATH = "metadata/chunks_metadata.csv"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EXPECTED_DIM = 384


def load_chunks():
    print("[A1] Loading processed document chunks...")
    df = pd.read_csv(CSV_PATH)

    required_cols = {"chunk_id", "chunk_text", "role", "source_path"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Missing required columns in chunks_metadata.csv")

    print(f"✔ Loaded {len(df)} chunks")
    return df


def load_model():
    print("[A2] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("✔ Model loaded")
    return model


def generate_embeddings(df, model):
    print("[A3] Generating embeddings...")
    texts = df["chunk_text"].astype(str).tolist()
    embeddings = model.encode(texts, convert_to_numpy=True)
    print("✔ Embeddings generated")
    return embeddings


def validate_embeddings(embeddings):
    print("[A4] Validating embeddings...")

    if embeddings.shape[1] != EXPECTED_DIM:
        raise ValueError("Embedding dimension mismatch")

    if np.isnan(embeddings).any():
        raise ValueError("NaN values found")

    if np.isinf(embeddings).any():
        raise ValueError("Infinite values found")

    print("✔ Embedding dimensions & integrity verified")


def temporary_store(df, embeddings):
    print("[A5] Storing embeddings temporarily (in memory)...")

    temp_store = {}
    for i, row in df.iterrows():
        temp_store[row["chunk_id"]] = {
            "embedding": embeddings[i],
            "role": row["role"],
            "source": row["source_path"]
        }

    print("✔ Temporary storage successful")
    return temp_store


def main():
    print("\n=== Milestone 2 | Embedding Validation ===\n")

    df = load_chunks()
    model = load_model()
    embeddings = generate_embeddings(df, model)
    validate_embeddings(embeddings)
    store = temporary_store(df, embeddings)

    sample = next(iter(store.values()))
    print("\nSample embedding dimension:", len(sample["embedding"]))
    print("\n✅ MODULE 3 VALIDATION COMPLETED\n")


if __name__ == "__main__":
    main()
