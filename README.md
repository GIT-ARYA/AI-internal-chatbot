# AI Company Internal Chatbot with Role-Based Access Control

This project implements a secure, role-based internal chatbot backend using semantic search and vector databases.  
The system ensures that users can access **only authorized internal documents** based on their assigned roles.

The implementation follows a **milestone-driven architecture**, aligned with enterprise-grade backend design principles.

---

## 🚀 Project Overview

The chatbot backend provides:

- Semantic search over internal company documents
- Role-Based Access Control (RBAC) enforced at search level
- Secure document retrieval before any response generation
- A strong foundation for Retrieval-Augmented Generation (RAG)

---

## 🧩 Tech Stack

- **Language:** Python 3.11
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB (Persistent Client)
- **Data Processing:** pandas
- **Testing:** Custom automated test suite
- **Architecture:** Modular, milestone-based

---

## 📁 Project Structure

project_root/
│
├── data_raw/ # Raw internal documents (.md, .csv)
│
├── metadata/
│ ├── chunks_metadata.csv # Chunked text with metadata
│ ├── doc_manifest.json # Parsed document manifest
│ └── role_document_map.yaml # Role → document mapping
│
├── chroma_db/ # Persistent vector database
│
├── src/
│ ├── utils.py
│ ├── parse_docs.py
│ ├── preprocess.py
│ ├── embeddings_index.py
│
│ ├── m2_embedding_validation.py
│ ├── m2_role_guard.py
│ ├── m2_retriever.py
│ ├── m2_test_cases.py
│ ├── m2_test_runner.py
│
├── quick_driver.py
├── Milestone1_Documentation.docx
├── Milestone2_Documentation.docx
└── README.md

---

## 🏁 Milestone 1: Data Preparation & Vectorization

### Objectives
- Parse internal documents
- Clean and normalize text
- Chunk documents with overlap
- Assign role-based metadata
- Generate embeddings
- Build a persistent vector database

### Key Outputs
- **147 document chunks**
- `chunks_metadata.csv`
- `role_document_map.yaml`
- Populated `chroma_db/`

### How to Run
```bash
python quick_driver.py
python src/embeddings_index.py
📄 Detailed documentation: Milestone1_Documentation.docx

🔐 Milestone 2: Backend Auth & Semantic Search
Module 3: Vector Database & Embedding Generation
Embedding model selection and validation

Verified embedding dimensions (384)

Indexed embeddings into ChromaDB

Implemented semantic search

Module 4: Role-Based Search & Query Processing
Strict RBAC enforced during retrieval

Secure role-filtered semantic search

Automated access validation tests

Role Hierarchy
mathematica
Copy code
Employees → Employees
HR → HR
Finance → Finance
Marketing → Marketing
Engineering → Engineering
C-Level → All roles
How to Run Validation & Tests
bash
Copy code
python src/m2_embedding_validation.py
python src/m2_role_guard.py
python src/m2_retriever.py
python src/m2_test_runner.py
📄 Detailed documentation: Milestone2_Documentation.docx

✅ Security Guarantees
Unauthorized document access is fully blocked

Role-based filtering occurs before any response generation

No cross-department data leakage

C-Level override access supported

All access rules validated using automated tests

🧪 Testing Summary
Total test cases: 5

Passed: 5

Failed: 0

All role-based access control scenarios passed successfully.

