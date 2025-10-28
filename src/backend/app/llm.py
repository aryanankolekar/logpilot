"""
llm.py — optional abstraction for local/remote model selection.
Currently routes all requests to Ollama for local inference.
"""

from .llm_ollama import query_local_llm


def run_llm(prompt: str):
    """Dispatch prompt to appropriate LLM backend (local)."""
    return query_local_llm(prompt)
