
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return titles, URLs, and content snippets."""

    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing from the root .env file.")

    if not query.strip():
        raise ValueError("Please provide a search query.")

    response = requests.post(
        TAVILY_URL,
        headers={
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        }
        for item in data.get("results", [])
    ]
