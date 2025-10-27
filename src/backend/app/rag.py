from .storage import vector_store_search
from .llm import generate_answer as extractive_generate

# attempt to import the ollama adapter
try:
    from .llm_ollama import ollama_generate
    _OLLAMA_AVAILABLE = True
except Exception:
    ollama_generate = None
    _OLLAMA_AVAILABLE = False


def _make_prompt_from_query_and_contexts(query: str, contexts: list[dict]) -> str:
    """
    Create a concise prompt for the LLM that includes the user query and
    the retrieved evidence chunks (as short citations).
    """
    lines = []
    lines.append(f"Answer the user query using ONLY the evidence below. If unsure, say you don't know.\n")
    lines.append(f"User query: {query}\n")
    lines.append("Evidence:")
    for i, c in enumerate(contexts, start=1):
        doc = c.get("doc_id", "<doc>")
        text = c.get("chunk_text", "").strip()
        lines.append(f"[{i}] {doc}: {text}")
    lines.append("\nPlease produce a short, factual answer. Then list which evidence lines you used (by index).")
    return "\n".join(lines)


def answer_query(query: str, k: int = 6, model: str = None) -> dict:
    # retrieve
    contexts = vector_store_search(query, k=k)

    # Try Ollama if available
    if _OLLAMA_AVAILABLE:
        print("OLLAMA_AVAILABLE:", _OLLAMA_AVAILABLE)
        prompt = _make_prompt_from_query_and_contexts(query, contexts)
        try:
            llm_resp = ollama_generate(prompt, model=model)
            text = llm_resp.get("text", "")
            return {
                "query": query,
                "answer": text,
                "confidence": 0.0,  # Ollama does not give a numeric confidence; we keep heuristic or add later
                "evidence": contexts,
                "llm_raw": llm_resp.get("raw"),
            }
        except Exception as e:
            # fall back to extractive summarizer and include the error for debugging
            fallback = extractive_generate(query, contexts)
            return {
                "query": query,
                "answer": fallback["text"],
                "confidence": fallback.get("confidence", 0.0),
                "evidence": contexts,
                "llm_error": str(e),
            }
    # Ollama not available — use extractive stub
    fallback = extractive_generate(query, contexts)
    return {
        "query": query,
        "answer": fallback["text"],
        "confidence": fallback.get("confidence", 0.0),
        "evidence": contexts,
    }
