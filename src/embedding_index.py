# src/embeddings_index.py
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_chunks(csv_path='metadata/chunks_metadata.csv'):
    return pd.read_csv(csv_path)

def index_to_chroma(csv_path='metadata/chunks_metadata.csv', persist_dir='chroma_db', batch_size=64):
    df = load_chunks(csv_path)
    texts = df['chunk_text'].astype(str).tolist()
    ids = df['chunk_id'].astype(str).tolist()
    metadatas = df[['source_path','role','start','end','seq']].to_dict(orient='records')

    # load model
    print("Loading embedding model:", MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)

    # Create PersistentClient (new API) - stores DB at `persist_dir`
    print("Creating Chroma PersistentClient at:", persist_dir)
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    settings = Settings()  # default settings; adjust if needed
    client = chromadb.PersistentClient(path=persist_dir, settings=settings,
                                       tenant=DEFAULT_TENANT, database=DEFAULT_DATABASE)

    # get or create collection
    try:
        collection = client.get_collection("company_docs")
    except Exception:
        collection = client.create_collection(name="company_docs")

    n = len(texts)
    print(f"Indexing {n} documents in batches of {batch_size}...")

    for i in range(0, n, batch_size):
        i2 = min(n, i + batch_size)
        batch_texts = texts[i:i2]
        batch_ids = ids[i:i2]
        batch_meta = metadatas[i:i2]

        # compute embeddings (as numpy)
        emb = model.encode(batch_texts, convert_to_numpy=True, show_progress_bar=False)
        # ensure list-of-lists
        emb_list = [e.tolist() for e in np.asarray(emb)]

        # add to collection
        collection.add(
            ids=batch_ids,
            documents=batch_texts,
            metadatas=batch_meta,
            embeddings=emb_list
        )
        print(f"Indexed batch {i}..{i2}")

    # Persist (client persists automatically, but ensure write)
    try:
        client.persist()
    except AttributeError:
        # some clients persist on close; ignore if method not present
        pass

    print("Indexing complete. Chroma persisted to", persist_dir)

if __name__ == '__main__':
    index_to_chroma()
