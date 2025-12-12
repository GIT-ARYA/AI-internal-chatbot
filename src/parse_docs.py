# parse_docs.py
import csv
import os
from pathlib import Path
from src.utils import clean_text, is_markdown, is_csv

def walk_data_dir(data_dir: str):
    p = Path(data_dir)
    for path in p.rglob('*'):
        if path.is_file() and (is_markdown(path) or is_csv(path)):
            yield path

def read_markdown(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    return clean_text(text)

def read_csv(path: Path, text_columns=None):
    # fallback: join all text columns
    rows = []
    import pandas as pd
    df = pd.read_csv(path)
    if text_columns is None:
        text_columns = [c for c in df.columns if df[c].dtype == object]
    for _, row in df.iterrows():
        parts = [str(row[c]) for c in text_columns if not pd.isna(row[c])]
        rows.append(clean_text("\n".join(parts)))
    return "\n\n".join(rows)

def parse_all(data_dir='data_raw'):
    docs = []
    for p in walk_data_dir(data_dir):
        if is_markdown(p):
            txt = read_markdown(p)
            docs.append({'path': str(p), 'type': 'md', 'text': txt})
        elif is_csv(p):
            txt = read_csv(p)
            docs.append({'path': str(p), 'type': 'csv', 'text': txt})
    return docs

if __name__ == '__main__':
    import json
    docs = parse_all('data_raw')
    print(f'Found {len(docs)} documents.')
    # optionally save a brief manifest
    with open('metadata/doc_manifest.json','w',encoding='utf-8') as f:
        json.dump([{'path':d['path'],'type':d['type'],'len':len(d['text'])} for d in docs], f, indent=2)
