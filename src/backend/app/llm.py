"""
Minimal local 'LLM' wrapper (extractive summarizer).
Replace later with a real local LLM adapter (Ollama / llama-cpp-python).
"""
from typing import List, Dict


def _summarize_extractive(query: str, contexts: List[Dict], max_sentences: int = 6) -> str:
    if not contexts:
        return "No relevant evidence found in the indexed logs."

    contexts_sorted = sorted(contexts, key=lambda c: c.get("score", 0.0))
    chosen = contexts_sorted[:max_sentences]

    lines = [f"Query: {query}", "Summary (extractive; evidence follows):"]
    for i, c in enumerate(chosen, start=1):
        snippet = c.get("chunk_text", "")[:600]
        lines.append(f"{i}. [{c.get('doc_id')}] {snippet}")
    return "\n".join(lines)


def generate_answer(query: str, contexts: List[Dict]) -> Dict:
    text = _summarize_extractive(query, contexts)
    confidence = 0.0
    if contexts:
        scores = [c.get("score", 1.0) for c in contexts if c.get("score") is not None]
        if scores:
            inv = [1.0 / (1.0 + s) for s in scores]
            confidence = float(min(1.0, max(0.0, sum(inv) / len(inv))))
        else:
            confidence = 0.2
    return {"text": text, "evidence": contexts, "confidence": confidence}
