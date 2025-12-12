# quick_driver.py

from src.parse_docs import parse_all
from src.preprocess import process_docs

# 1. Parse documents inside data_raw/
docs = parse_all('data_raw')

# 2. Chunk them + assign metadata + save to chunks_metadata.csv
process_docs(docs, out_csv='metadata/chunks_metadata.csv')

print("Milestone 1: Parsing + Chunking Completed Successfully!")
