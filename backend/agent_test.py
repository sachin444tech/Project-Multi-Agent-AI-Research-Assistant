
from agent import ask_agent


if __name__ == "__main__":
    question = (
        "Explain a Multi-Agent AI Research Assistant "
        "in exactly three simple bullet points."
    )

    print("\nAsking the AI research agent...\n")

    try:
        answer = ask_agent(question)
        print("AI AGENT RESPONSE:\n")
        print(answer)

    except Exception as error:
        print(f"\nThe test failed: {error}")
