import re
from pathlib import Path

def clean_text(text: str) -> str:
    # basic normalization
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\n{2,}', '\n\n', text)  # collapse multiple newlines
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = text.strip()
    return text

def chunk_text(text: str, max_chars=1000, overlap=200):
    """
    Approximate chunking: max_chars ~ 1000 chars ~ ~300 tokens (approx).
    Returns list of (chunk_text, start_idx, end_idx)
    """
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = start + max_chars
        if end >= n:
            chunk = text[start:n].strip()
            chunks.append((chunk, start, n))
            break
        # try to end at newline or space to avoid splitting words
        slice_end = text.rfind('\n', start, end)
        if slice_end <= start:
            slice_end = text.rfind(' ', start, end)
        if slice_end <= start:
            slice_end = end
        chunk = text[start:slice_end].strip()
        chunks.append((chunk, start, slice_end))
        start = slice_end - overlap  # overlap
    return chunks

def is_markdown(file_path: Path) -> bool:
    return file_path.suffix.lower() in ['.md', '.markdown', '.txt']

def is_csv(file_path: Path) -> bool:
    return file_path.suffix.lower() == '.csv'
