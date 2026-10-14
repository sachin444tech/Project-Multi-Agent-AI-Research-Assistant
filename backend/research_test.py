
from research import search_web

if __name__ == "__main__":
    query = "Recent applications of multi-agent AI systems"

    try:
        results = search_web(query)

        if not results:
            print("No results found.")
        else:
            for number, item in enumerate(results, start=1):
                print(f"\n{number}. {item['title']}")
                print(f"URL: {item['url']}")
                print(f"Summary: {item['content'][:400]}")

    except Exception as error:
        print(f"Search failed: {error}")
