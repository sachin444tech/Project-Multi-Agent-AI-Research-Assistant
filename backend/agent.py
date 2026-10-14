
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-3.5-lightning:free"


def ask_agent(question: str) -> str:
    """Send a question to the AI model and return its text answer."""

    if not API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing from the root .env file."
        )

    if not question.strip():
        raise ValueError("Please enter a question.")

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
                "You are a concise AI research assistant. "
                "Answer using clear text and simple language. "
                "Keep internal reasoning brief and provide the final answer."
            ),
        },
        {"role": "user", "content": question},
    ],
    "max_tokens": 1500,
}


    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=90,
    )

    response.raise_for_status()
    data = response.json()

    choices = data.get("choices", [])

    if not choices:
        raise RuntimeError(
            f"OpenRouter returned no choices. Response: {data}"
        )

    choice = choices[0]
    message = choice.get("message", {})
    content = message.get("content")

    # Most models return their answer as a string.
    if isinstance(content, str) and content.strip():
        return content.strip()

    # Some responses represent text as a list of content blocks.
    if isinstance(content, list):
        text_parts = [
            item["text"]
            for item in content
            if isinstance(item, dict)
            and isinstance(item.get("text"), str)
        ]

        if text_parts:
            return "\n".join(text_parts).strip()

    # Print diagnostics if the model returned no usable text.
    print("Model returned no usable text.")
    print("Finish reason:", choice.get("finish_reason"))
    print("Message fields:", list(message.keys()))
    print("Response error:", data.get("error"))

    raise RuntimeError(
        "The AI model returned no text answer. "
        "Review the diagnostic information above."
    )

