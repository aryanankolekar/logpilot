"""
llm_ollama.py — communicate with local Ollama model.
"""

import requests
import json
from .config import settings


def query_local_llm(prompt: str):
    """Send prompt to local Ollama instance and return output text."""
    try:
        payload = {
            "model": settings.LLM_MODEL,
            "messages": [
                {"role": "system", "content": "You are LogCopilot, an expert in analyzing logs, deciphering patterns and helping user with their log related queries. Always answer in plaintext - do not use markdown."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        response = requests.post(
            settings.LLM_ENDPOINT,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=300
        )

        if response.status_code != 200:
            return None, f"Ollama HTTP {response.status_code}: {response.text}"

        data = response.json()
        text = data.get("message", {}).get("content", "") or data.get("content", "")
        return text.strip(), None

    except requests.exceptions.ConnectionError:
        return None, f"Cannot connect to Ollama at {settings.LLM_ENDPOINT}"
    except requests.exceptions.Timeout:
        return None, "Timeout waiting for Ollama"
    except Exception as e:
        return None, str(e)