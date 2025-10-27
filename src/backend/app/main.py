from fastapi import FastAPI, HTTPException, UploadFile, File
from pathlib import Path
import uvicorn
import threading
from .config import settings
from .rag import answer_query
from .ingest import start_watch
from .storage import vector_store_upsert


app = FastAPI(title="Copilot Log Assistant - Backend")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ingest/upload")
async def ingest_upload(file: UploadFile = File(...)):
    data = await file.read()
    path = Path(settings.LOG_DIR) / file.filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

    text = data.decode("utf-8", errors="ignore")
    count = vector_store_upsert(file.filename, text)
    return {"status": "ok", "filename": str(path), "chunks_indexed": count}


@app.post("/query")
async def query(payload: dict):
    q = payload.get("q") or payload.get("query")
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' in payload")
    result = answer_query(q)
    return result


if __name__ == "__main__":
    t = threading.Thread(target=lambda: start_watch(Path(settings.LOG_DIR)), daemon=True)
    t.start()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
