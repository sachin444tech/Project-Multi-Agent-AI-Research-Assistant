
from research_agent import conduct_research


if __name__ == "__main__":
    question = "How are multi-agent AI systems used in scientific research?"

    print("\nResearching your question. Please wait...\n")

    try:
        report = conduct_research(question)

        print("=" * 60)
        print("RESEARCH QUESTION")
        print("=" * 60)
        print(report["question"])

        print("\n" + "=" * 60)
        print("AI RESEARCH REPORT")
        print("=" * 60)
        print(report["answer"])

        print("\n" + "=" * 60)
        print("SOURCES")
        print("=" * 60)

        for number, source in enumerate(report["sources"], start=1):
            print(f"\n[{number}] {source['title']}")
            print(source["url"])

    except Exception as error:
        print(f"\nResearch failed: {error}")
