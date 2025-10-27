"""
main.py — FastAPI entry point for LogCopilot backend.
"""

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
from .config import settings
from .rag import answer_query
from .ingest import ingest_file, start_watch

app = FastAPI(title="LogCopilot", version="1.0")


@app.on_event("startup")
async def startup_event():
    print("[Startup] Launching log watcher...")
    start_watch()


@app.get("/health")
def health():
    return {"status": "ok", "message": "LogCopilot backend running."}


@app.post("/ingest/upload")
async def upload_log(file: UploadFile = File(...)):
    """Manual upload endpoint for testing ingestion."""
    dest = Path(settings.LOG_DIR) / file.filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ingest_file(dest)
    return {"message": f"Ingested {file.filename}"}


@app.post("/query")
async def query_logs(payload: dict):
    """RAG-style query endpoint."""
    query = payload.get("query")
    if not query:
        return {"error": "Missing query."}
    return answer_query(query)
