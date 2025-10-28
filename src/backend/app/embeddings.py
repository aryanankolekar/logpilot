"""
embeddings.py — handles text embeddings for LogCopilot.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from .config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        print(f"[Embeddings] Loading model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str):
    """Embed a single query or sentence."""
    model = get_model()
    cleaned = " ".join(text.split())
    vector = model.encode(cleaned, show_progress_bar=False)
    return np.array(vector, dtype="float32")


def embed_chunks(chunks: list[str]):
    """Embed multiple log text chunks in batch."""
    model = get_model()
    embeddings = model.encode(chunks, show_progress_bar=False)
    return np.array(embeddings, dtype="float32")