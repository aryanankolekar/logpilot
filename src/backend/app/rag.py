"""
RAG orchestration: retrieve top-k chunks from vector store and call LLM wrapper.
"""
from .storage import vector_store_search
from .llm import generate_answer


def answer_query(query: str, k: int = 6) -> dict:
    contexts = vector_store_search(query, k=k)
    llm_out = generate_answer(query, contexts)
    return {
        "query": query,
        "answer": llm_out["text"],
        "confidence": llm_out.get("confidence", 0.0),
        "evidence": llm_out.get("evidence", []),
    }
