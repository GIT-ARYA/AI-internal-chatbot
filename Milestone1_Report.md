# Milestone 1 Report

**Summary**

- Documents parsed (manifest entries): 10

- Total chunks created: 147

- Embedding model used: sentence-transformers/all-MiniLM-L6-v2

- Vector DB: Chroma (persisted at ./chroma_db)


**Role counts**

- Marketing: 46

- Engineering: 38

- Finance: 27

- Employees: 19

- Hr: 17


**Role → source files (sample)**

- Employees: 1 files (examples: ['data_raw\\general\\employee_handbook.md'])

- Engineering: 1 files (examples: ['data_raw\\engineering\\engineering_master_doc.md'])

- Finance: 2 files (examples: ['data_raw\\Finance\\financial_summary.md', 'data_raw\\Finance\\quarterly_financial_report.md'])

- Hr: 1 files (examples: ['data_raw\\HR\\hr_data.csv'])

- Marketing: 5 files (examples: ['data_raw\\marketing\\market_report_q4_2024.md', 'data_raw\\marketing\\marketing_report_2024.md', 'data_raw\\marketing\\marketing_report_q1_2024.md', 'data_raw\\marketing\\marketing_report_q2_2024.md', 'data_raw\\marketing\\marketing_report_q3_2024.md'])


**Notes / assumptions**

- Role assignment was inferred from file path folder names (see role_document_map.yaml).

- Chunking used character-based chunking with overlap; chunk size ~1000 chars (approx 300 tokens).
