"""
storage.py — persistent FAISS + metadata store for LogCopilot.
"""

import json
import faiss
import numpy as np
from pathlib import Path
from typing import List
from .config import settings

INDEX_DIR = Path(settings.VECTOR_STORE_PATH)
FAISS_PATH = INDEX_DIR / "faiss.index"
META_PATH = INDEX_DIR / "metadata.json"

INDEX_DIR.mkdir(parents=True, exist_ok=True)

_index = None
_metadata = []


def load_index():
    """Load or initialize FAISS index."""
    global _index, _metadata
    if FAISS_PATH.exists():
        _index = faiss.read_index(str(FAISS_PATH))
        print(f"[Storage] Loaded FAISS index from {FAISS_PATH}")
    else:
        _index = faiss.IndexFlatL2(384)
        print("[Storage] Created new FAISS index (384d)")

    if META_PATH.exists():
        with open(META_PATH, "r", encoding="utf-8") as f:
            _metadata = json.load(f)
    else:
        _metadata = []


def save_index():
    """Persist FAISS index + metadata."""
    if _index is None:
        return
    faiss.write_index(_index, str(FAISS_PATH))
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(_metadata, f, indent=2)
    print("[Storage] Saved FAISS index + metadata")


def add_to_index(vectors: np.ndarray, chunks: List[str], source_file: str):
    """Add embeddings and metadata to FAISS."""
    global _index, _metadata
    if _index is None:
        load_index()

    vectors = np.array(vectors, dtype="float32")
    _index.add(vectors)

    for c in chunks:
        _metadata.append({"source": source_file, "chunk": c[:200]})

    save_index()


def search_index(query_vector: np.ndarray, k: int = 5):
    """Retrieve nearest chunks by vector similarity."""
    global _index, _metadata
    if _index is None:
        load_index()

    query_vector = np.array(query_vector, dtype="float32").reshape(1, -1)
    distances, indices = _index.search(query_vector, k)

    results = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(_metadata):
            results.append({
                "id": int(idx),
                "score": float(distances[0][i]),
                "doc_id": _metadata[idx]["source"],
                "chunk_text": _metadata[idx]["chunk"],
            })
    return results
