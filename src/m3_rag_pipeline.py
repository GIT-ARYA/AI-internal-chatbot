# src/m3_rag_pipeline.py

"""
Milestone 3 – RAG Pipeline
Secure Retrieval + Prompt Builder + LLM
"""

from m2_retriever import secure_retrieve
from m3_prompt_builder import build_prompt
from m3_llm_client import call_llm


def ask(query, user_role, top_k=5):
    """
    End-to-end RAG pipeline.
    """

    print("\n=== RAG PIPELINE START ===")
    print(f"User Role: {user_role}")
    print(f"Query: {query}")

    # Step 1: Secure retrieval (RBAC enforced)
    retrieved_chunks = secure_retrieve(query, user_role, top_k=top_k)

    # Step 2: Prompt construction
    prompt = build_prompt(query, retrieved_chunks)

    # Step 3: LLM answer generation
    answer = call_llm(prompt)

    print("\n=== RAG PIPELINE END ===\n")

    return answer


if __name__ == "__main__":
    # Demo test
    print(
        ask(
            "What is the quarterly financial performance?",
            user_role="Finance"
        )
    )

    print(
        ask(
            "What is the quarterly financial performance?",
            user_role="Marketing"
        )
    )
