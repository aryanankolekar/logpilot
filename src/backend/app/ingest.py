"""
ingest.py — handles log ingestion and recursive directory watching.
"""

import os
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config import settings
from .embeddings import embed_chunks
from .storage import add_to_index


def chunk_text(text: str, max_len: int = 500):
    """Split log text into smaller overlapping chunks."""
    words, chunks, current = text.split(), [], []
    for word in words:
        current.append(word)
        if len(current) >= max_len:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


def ingest_file(file_path: Path):
    """Ingest a single log file into FAISS."""
    try:
        if not file_path.exists() or not file_path.is_file():
            return
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if not content.strip():
            return

        chunks = chunk_text(content)
        vectors = embed_chunks(chunks)
        add_to_index(vectors, chunks, source_file=file_path.name)
        print(f"[Ingest] ✅ Indexed {len(chunks)} chunks from {file_path.name}")
    except Exception as e:
        print(f"[Ingest] ❌ Error: {file_path} → {e}")


def ingest_directory(directory: Path):
    """Recursively ingest all .txt/.log files."""
    for root, _, files in os.walk(directory):
        for fname in files:
            if fname.endswith((".txt", ".log")):
                ingest_file(Path(root) / fname)


class LogHandler(FileSystemEventHandler):
    """File watcher callback for new or modified log files."""

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith((".txt", ".log")):
            file_path = Path(event.src_path)
            print(f"[Watcher] New file: {file_path.name}")
            ingest_file(file_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith((".txt", ".log")):
            file_path = Path(event.src_path)
            print(f"[Watcher] Modified: {file_path.name}")
            ingest_file(file_path)


def start_watch():
    """Launch recursive directory watcher in background."""
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, str(log_dir), recursive=True)
    t = threading.Thread(target=observer.start)
    t.daemon = True
    t.start()
    print(f"[Watcher] Monitoring logs recursively under: {log_dir.resolve()}")