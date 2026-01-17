# src/m3_chat_cli.py

"""
Milestone 3 – CLI Chatbot
Secure role-based chatbot demo
"""

from m3_rag_pipeline import ask


def main():
    print("\n=== Secure Internal Chatbot (CLI) ===\n")

    role = input(
        "Enter your role "
        "(Employees / HR / Finance / Marketing / Engineering / C-Level): "
    ).strip()

    print("\nType 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\nGoodbye 👋")
            break

        try:
            answer = ask(query, role)
            print("\nAssistant:")
            print(answer)
            print("\n" + "-" * 60 + "\n")

        except Exception as e:
            print("\n❌ Error:", e)
            print("-" * 60)


if __name__ == "__main__":
    main()
