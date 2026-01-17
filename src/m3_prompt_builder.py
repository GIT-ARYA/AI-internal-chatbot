# src/m3_prompt_builder.py

"""
Milestone 3 – Prompt Builder
Constructs safe prompts using only authorized document chunks.
"""

MAX_CONTEXT_CHARS = 3000


def build_prompt(query, retrieved_chunks):
    """
    Builds a controlled prompt for the LLM.
    Only authorized chunks are included.
    """

    # Case 1: No authorized data
    if not retrieved_chunks:
        return (
            "You are an internal company assistant.\n\n"
            "The user asked:\n"
            f"{query}\n\n"
            "You do not have access to the required information.\n"
            "Respond politely that the information is unavailable."
        )

    # Case 2: Authorized context exists
    context = ""
    for chunk in retrieved_chunks:
        text = chunk["text"].strip()
        if len(context) + len(text) > MAX_CONTEXT_CHARS:
            break
        context += text + "\n\n"

    prompt = f"""
You are an internal company assistant.
Answer the user's question strictly using the context below.
If the answer is not present, say you do not have access.

Context:
{context}

Question:
{query}

Answer:
""".strip()

    return prompt
