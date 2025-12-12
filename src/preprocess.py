# preprocess.py
import csv
import os
from pathlib import Path
from src.utils import chunk_text
import json

def assign_role_from_path(path_str):
    # simple heuristic: folder name decides role
    p = Path(path_str)
    parts = [pp.lower() for pp in p.parts]
    for role in ['finance','marketing','hr','engineering','general','employees','c-level','c_level','clevel']:
        if any(role in part for part in parts):
            if role in ['general','employees']:
                return 'Employees'
            if role in ['c-level','c_level','clevel']:
                return 'C-Level'
            return role.capitalize()
    # default fallback
    return 'Employees'

def process_docs(docs, out_csv='metadata/chunks_metadata.csv'):
    Path('metadata').mkdir(exist_ok=True)
    with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['chunk_id','source_path','role','chunk_text','start','end','seq'])
        writer.writeheader()
        seq = 0
        for doc in docs:
            role = assign_role_from_path(doc['path'])
            chunks = chunk_text(doc['text'], max_chars=1000, overlap=200)
            for i,(chunk, start, end) in enumerate(chunks):
                chunk_id = f"{Path(doc['path']).stem}__{seq}"
                writer.writerow({
                    'chunk_id': chunk_id,
                    'source_path': doc['path'],
                    'role': role,
                    'chunk_text': chunk,
                    'start': start,
                    'end': end,
                    'seq': seq
                })
                seq += 1
    print(f"Written chunks to {out_csv}. Total chunks: {seq}")

if __name__ == '__main__':
    import json
    with open('metadata/doc_manifest.json','r',encoding='utf-8') as f:
        manifest = json.load(f)
    # to proceed, re-load full texts via parse_docs or save full docs earlier
    # For simplicity, run parse_docs and pass docs directly when invoking this module programmatically
    print("Run preprocess via driver script or import.")
