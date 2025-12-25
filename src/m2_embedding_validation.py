# src/m2_embedding_validation.py

"""
Milestone 2 – Phase A
Step A1–A5: Embedding & Data Validation
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

CSV_PATH = "metadata/chunks_metadata.csv"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EXPECTED_DIM = 384   # MiniLM-L6-v2 embedding dimension


def load_chunks(csv_path):
    print("[A2] Loading processed document chunks...")
    df = pd.read_csv(csv_path)

    required_cols = {"chunk_id", "chunk_text", "role", "source_path"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # basic validation
    if df["chunk_text"].isnull().any():
        raise ValueError("Empty chunk_text found")

    print(f"✔ Loaded {len(df)} chunks successfully")
    return df


def load_embedding_model():
    print("[A1] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("✔ Model loaded:", MODEL_NAME)
    return model


def generate_embeddings(df, model):
    print("[A3] Generating embeddings (temporary, in-memory)...")
    texts = df["chunk_text"].astype(str).tolist()
    embeddings = model.encode(texts, convert_to_numpy=True)

    print(f"✔ Generated embeddings for {len(embeddings)} chunks")
    return embeddings


def verify_embeddings(embeddings):
    print("[A4] Verifying embedding dimensions and integrity...")

    # shape check
    if len(embeddings.shape) != 2:
        raise ValueError("Embeddings must be 2D array")

    dim = embeddings.shape[1]
    if dim != EXPECTED_DIM:
        raise ValueError(f"Invalid embedding dimension: {dim} (expected {EXPECTED_DIM})")

    # NaN / Inf check
    if np.isnan(embeddings).any():
        raise ValueError("NaN values found in embeddings")

    if np.isinf(embeddings).any():
        raise ValueError("Infinite values found in embeddings")

    print(f"✔ All embeddings have correct dimension ({EXPECTED_DIM})")
    print("✔ No NaN or Inf values found")


def store_embeddings_temporarily(df, embeddings):
    print("[A5] Storing embeddings temporarily (not persisted)...")

    temp_store = {}

    for idx, row in df.iterrows():
        temp_store[row["chunk_id"]] = {
            "embedding": embeddings[idx],
            "role": row["role"],
            "source_path": row["source_path"]
        }

    print(f"✔ Stored {len(temp_store)} embeddings in temporary memory")
    return temp_store


def main():
    print("\n=== Milestone 2 | Phase A: Embedding Validation ===\n")

    df = load_chunks(CSV_PATH)
    model = load_embedding_model()
    embeddings = generate_embeddings(df, model)
    verify_embeddings(embeddings)
    temp_embeddings = store_embeddings_temporarily(df, embeddings)

    print("\n✅ PHASE A COMPLETED SUCCESSFULLY")
    print("Embeddings validated and ready for secure retrieval testing.\n")

    # optional: inspect one sample
    sample_key = next(iter(temp_embeddings))
    print("Sample embedding info:")
    print("chunk_id:", sample_key)
    print("role:", temp_embeddings[sample_key]["role"])
    print("embedding_dim:", len(temp_embeddings[sample_key]["embedding"]))


if __name__ == "__main__":
    main()
