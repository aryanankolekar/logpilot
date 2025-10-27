"""
Ollama adapter for local LLM integration.

Usage:
    from .llm_ollama import ollama_generate
    resp = ollama_generate(prompt, model="llama3.2", timeout=30)

This calls http://localhost:11434/api/chat by default (Ollama's local API).
If Ollama is not reachable, it raises a RuntimeError so caller can fallback.
"""
import requests
import json
from typing import List, Dict, Optional

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.2"
DEFAULT_TIMEOUT = 120  # seconds


def _build_messages_from_prompt(prompt: str) -> List[Dict]:
    # Ollama chat expects messages list with roles
    return [{"role": "user", "content": prompt}]


def ollama_generate(
    prompt: str,
    model: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    stream: bool = False,
) -> Dict:
    """
    Send a chat request to the local Ollama server and return parsed result.
    Returns a dict with keys: 'text' (str), 'raw' (full response JSON).
    Raises RuntimeError if Ollama is not reachable.
    """
    model = model or DEFAULT_MODEL
    payload = {
        "model": model,
        "messages": _build_messages_from_prompt(prompt),
        "stream": stream,
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to reach Ollama at {OLLAMA_URL}: {e}")

    if r.status_code != 200:
        # include body for debugging
        raise RuntimeError(f"Ollama returned HTTP {r.status_code}: {r.text}")

    try:
        data = r.json()
    except ValueError:
        raise RuntimeError(f"Ollama returned non-JSON response: {r.text}")

    # Ollama chat responses often return 'choices' or 'response'; be defensive
    text = ""
    # try common response shapes
    if isinstance(data, dict):
        # new API: data may include 'choices' array with 'message' or 'content'
        if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
            first = data["choices"][0]
            # support nested message structure
            text = first.get("message", {}).get("content") or first.get("text") or first.get("content") or ""
        # older API shape: { "id":..., "model":..., "response": { "content": "..." } }
        if not text and "response" in data and isinstance(data["response"], dict):
            text = data["response"].get("content", "") or data["response"].get("text", "")
        # fallback: some endpoints return direct 'text' key
        if not text and "text" in data:
            text = data["text"]
    # if still empty, stringify the response
    if not text:
        text = json.dumps(data)

    return {"text": text, "raw": data}
