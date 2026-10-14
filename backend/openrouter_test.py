import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("API key not found in the root .env file.")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "nvidia/nemotron-3.5-lightning:free",
    "messages": [
        {
            "role": "user",
            "content": (
                "Explain a Multi-Agent AI Research Assistant "
                "in exactly three simple bullet points."
            ),
        }
    ],
    "max_tokens": 500,
    "reasoning": {"effort": "low"},
}

print("Testing the OpenRouter free model...")

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90,
    )

    if response.status_code == 200:
        result = response.json()
        message = result["choices"][0]["message"]
        answer = message.get("content")

        if answer:
            print("\nSUCCESS! The model responded:\n")
            print(answer)
        else:
            print("\nThe API worked, but returned no normal text.")
            print("Finish reason:", result["choices"][0].get("finish_reason"))
            print("Please try another free model if this continues.")

    else:
        print("\nAPI status:", response.status_code)
        print(response.text[:1500])

except requests.RequestException as error:
    print("\nConnection error:", error)
