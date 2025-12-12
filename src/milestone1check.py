# src/milestone1_inspect.py
import pandas as pd
from pathlib import Path
import yaml
import json
from collections import Counter

CSV = Path('metadata/chunks_metadata.csv')
MANIFEST = Path('metadata/doc_manifest.json')
ROLE_MAP_OUT = Path('metadata/role_document_map.yaml')
REPORT_OUT = Path('Milestone1_Report.md')

def load_csv():
    if not CSV.exists():
        print("ERROR: metadata/chunks_metadata.csv not found. Run quick_driver.py first.")
        return None
    df = pd.read_csv(CSV)
    return df

def build_role_map(df):
    role_map = {}
    for _, row in df.iterrows():
        role = str(row.get('role','Employees'))
        src = str(row.get('source_path','unknown'))
        role_map.setdefault(role, set()).add(src)
    # convert sets to sorted lists
    role_map = {r: sorted(list(s)) for r,s in role_map.items()}
    return role_map

def save_role_map(role_map):
    ROLE_MAP_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(ROLE_MAP_OUT, 'w', encoding='utf-8') as f:
        yaml.safe_dump(role_map, f, sort_keys=True, allow_unicode=True)
    print("Wrote role document map to", ROLE_MAP_OUT)

def create_report(df, role_map):
    num_chunks = len(df)
    roles = df['role'].fillna('Employees').astype(str).tolist()
    role_counts = Counter(roles)
    num_docs = 0
    manifest = {}
    if MANIFEST.exists():
        try:
            manifest = json.load(open(MANIFEST,'r',encoding='utf-8'))
            num_docs = len(manifest)
        except Exception:
            num_docs = None

    lines = []
    lines.append("# Milestone 1 Report\n")
    lines.append("**Summary**\n")
    lines.append(f"- Documents parsed (manifest entries): {num_docs}\n")
    lines.append(f"- Total chunks created: {num_chunks}\n")
    lines.append(f"- Embedding model used: sentence-transformers/all-MiniLM-L6-v2\n")
    lines.append(f"- Vector DB: Chroma (persisted at ./chroma_db)\n")
    lines.append("\n**Role counts**\n")
    for r,c in role_counts.most_common():
        lines.append(f"- {r}: {c}\n")
    lines.append("\n**Role → source files (sample)**\n")
    for r, files in sorted(role_map.items()):
        sample_files = files[:5]
        lines.append(f"- {r}: {len(files)} files (examples: {sample_files})\n")

    lines.append("\n**Notes / assumptions**\n")
    lines.append("- Role assignment was inferred from file path folder names (see role_document_map.yaml).\n")
    lines.append("- Chunking used character-based chunking with overlap; chunk size ~1000 chars (approx 300 tokens).\n")

    REPORT_OUT.write_text("\n".join(lines), encoding='utf-8')
    print("Wrote report to", REPORT_OUT)

def show_samples(df, n=3):
    print("\n=== SAMPLE CHUNKS (first {} chunks) ===\n".format(n))
    for idx,row in df.head(n).iterrows():
        print(f"chunk_id: {row.get('chunk_id')}")
        print(f"role: {row.get('role')}")
        print(f"source_path: {row.get('source_path')}")
        text = str(row.get('chunk_text','')).strip()
        print("text (first 400 chars):")
        print(text[:400].replace('\n',' ') + ("..." if len(text)>400 else ""))
        print("-"*60)

def main():
    df = load_csv()
    if df is None:
        return
    role_map = build_role_map(df)
    save_role_map(role_map)
    create_report(df, role_map)
    show_samples(df, n=5)
    print("\nDone. You can open metadata/role_document_map.yaml and Milestone1_Report.md")

if __name__ == '__main__':
    main()
