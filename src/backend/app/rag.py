"""
rag.py — core Retrieval-Augmented Generation logic.
"""

from typing import Dict, Any
from .embeddings import embed_text
from .storage import search_index
from .llm import run_llm


def answer_query(query: str) -> Dict[str, Any]:
    """Perform retrieval + local LLM reasoning."""
    query_vec = embed_text(query)
    results = search_index(query_vec, k=5)

    context = "\n".join([r["chunk_text"] for r in results])
    prompt = f"""
You are LogCopilot, a distributed system log analyst.
Analyze the following retrieved logs and answer the query.

Query: {query}

Logs:
{context}

Respond with a concise summary of findings, root causes, and notable patterns.
"""

    llm_response, llm_error = run_llm(prompt)

    return {
        "query": query,
        "answer": llm_response or "No clear answer found in retrieved context.",
        "confidence": float(len(results)) / 5.0,
        "evidence": results,
        "llm_error": llm_error,
    }