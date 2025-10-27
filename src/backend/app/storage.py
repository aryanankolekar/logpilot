"""
Durable FAISS + SQLite metadata store.
"""
from pathlib import Path
import sqlite3
import numpy as np
import faiss
from typing import List, Dict
from .embeddings import embed_texts
from .config import settings

VECTOR_DIR = Path(settings.VECTOR_DIR)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = VECTOR_DIR / "faiss.index"
DB_PATH = VECTOR_DIR / "metadata.db"

_index: faiss.Index = None
_conn: sqlite3.Connection = None
_default_dim = None


def _init_db():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(str(DB_PATH))
        cur = _conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY,
                doc_id TEXT,
                chunk_text TEXT
            )
            """
        )
        _conn.commit()
    return _conn


def _load_index(dim: int):
    global _index
    if _index is not None:
        return _index
    if INDEX_PATH.exists():
        try:
            _index = faiss.read_index(str(INDEX_PATH))
            return _index
        except Exception:
            pass
    _index = faiss.IndexFlatL2(dim)
    return _index


def _persist_index():
    if _index is not None:
        faiss.write_index(_index, str(INDEX_PATH))


def _chunk_text(text: str, max_chars: int = 512) -> List[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks, cur, cur_len = [], [], 0
    for line in lines:
        if cur_len + len(line) > max_chars and cur:
            chunks.append(" ".join(cur))
            cur, cur_len = [line], len(line)
        else:
            cur.append(line)
            cur_len += len(line)
    if cur:
        chunks.append(" ".join(cur))
    return chunks[:2000]


def vector_store_upsert(doc_id: str, text: str) -> int:
    global _default_dim
    conn = _init_db()
    chunks = _chunk_text(text, max_chars=settings.CHUNK_SIZE)
    if not chunks:
        return 0

    embeddings = embed_texts(chunks)
    dim = len(embeddings[0])
    _default_dim = _default_dim or dim
    idx = _load_index(dim)

    start_id = int(idx.ntotal)
    arr = np.array(embeddings).astype("float32")
    idx.add(arr)
    _persist_index()

    cur = conn.cursor()
    for i, chunk in enumerate(chunks):
        cur.execute(
            "INSERT INTO metadata (id, doc_id, chunk_text) VALUES (?, ?, ?)",
            (start_id + i, doc_id, chunk),
        )
    conn.commit()
    return len(chunks)


def vector_store_search(query: str, k: int = 5) -> List[Dict]:
    conn = _init_db()
    q_emb = embed_texts([query])[0]
    dim = len(q_emb)
    idx = _load_index(dim)
    if idx.ntotal == 0:
        return []

    q_vec = np.array([q_emb]).astype("float32")
    D, I = idx.search(q_vec, k)
    results = []
    for score, iid in zip(D[0].tolist(), I[0].tolist()):
        if iid < 0:
            continue
        cur = conn.cursor()
        cur.execute("SELECT doc_id, chunk_text FROM metadata WHERE id = ?", (int(iid),))
        row = cur.fetchone()
        if row:
            doc_id, chunk_text = row
            results.append(
                {"id": int(iid), "doc_id": doc_id, "chunk_text": chunk_text, "score": float(score)}
            )
    return results
