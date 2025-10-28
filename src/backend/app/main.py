from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .rag import answer_query
from .ingest import start_watch
from .log_utils import get_aggregated_log_stats
import threading

app = FastAPI(title="LogPilot Backend")

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_endpoint(request: Request):
    """Main query endpoint"""
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return JSONResponse({"error": "Missing query"}, status_code=400)
    result = answer_query(query)
    return JSONResponse(result)

@app.get("/")
def health():
    return {"status": "ok"}

# Background thread to watch log directory
def start_background_watch():
    watcher_thread = threading.Thread(target=start_watch, daemon=True)
    watcher_thread.start()

@app.on_event("startup")
def startup_event():
    start_background_watch()

# Endpoint for log statistics
@app.get("/api/stats")
async def get_system_stats():
    """
    Returns aggregated log analytics data for the visualization panel.
    """
    return get_aggregated_log_stats()
