# src/m3_llm_client.py

"""
Milestone 3 – LLM Client
Uses Groq API (Free Tier)
"""

import os
from groq import Groq

MODEL = "llama-3.1-8b-instant"


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not set. Please set your Groq API key."
        )
    return Groq(api_key=api_key)


def call_llm(prompt, max_tokens=256):
    """
    Sends prompt to Groq LLM and returns generated response text.
    """

    client = get_client()

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful internal company assistant. "
                    "Answer strictly based on the provided context. "
                    "If information is missing, say you do not have access."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=max_tokens,
    )

    return completion.choices[0].message.content.strip()
