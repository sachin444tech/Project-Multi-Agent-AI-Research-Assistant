
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Locate the project root and load its .env file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-3.5-lightning:free"


def ask_agent(question: str) -> str:
    """Send a question to the AI agent and return its answer."""

    if not API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing from the root .env file."
        )

    if not question.strip():
        raise ValueError("Please enter a research question.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI research assistant. "
                    "Answer clearly, accurately, and in simple language. "
                    "Do not invent facts or sources."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        "max_tokens": 700,
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=90,
    )

    response.raise_for_status()
    data = response.json()

    answer = data["choices"][0]["message"].get("content")

    if not answer:
        raise RuntimeError("The AI model returned no text answer.")

    return answer.strip()
