from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .rag import answer_query
from .ingest import start_watch
import threading

app = FastAPI(title="LogPilot Backend")

# ✅ Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # <-- this fixes the 405 OPTIONS issue
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

# ✅ Background thread to watch log directory
def start_background_watch():
    watcher_thread = threading.Thread(target=start_watch, daemon=True)
    watcher_thread.start()

@app.on_event("startup")
def startup_event():
    start_background_watch()
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .rag import answer_query
from .ingest import start_watch
import random
import datetime

app = FastAPI(title="LogPilot Copilot Backend")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Existing routes ---
@app.post("/query")
async def query_logs(payload: dict):
    query = payload.get("query", "")
    return await answer_query(query)

@app.on_event("startup")
async def startup_event():
    start_watch()

# --- NEW MOCKED ANALYTICS ENDPOINT ---
@app.get("/api/stats")
async def get_system_stats():
    """
    Returns mock log analytics data for visualization panel.
    This will later be replaced by real-time parsed log aggregation.
    """
    now = datetime.datetime.utcnow()

    # Mock severity distribution
    severity_counts = {
        "INFO": random.randint(200, 500),
        "WARN": random.randint(10, 30),
        "ERROR": random.randint(5, 20),
        "CRITICAL": random.randint(0, 5)
    }

    # Mock subsystem error counts
    errors_by_component = {
        "inference": random.randint(0, 10),
        "kube": random.randint(0, 5),
        "apache": random.randint(0, 3),
        "db": random.randint(0, 2),
        "auth": random.randint(0, 4)
    }

    # Mock timeline for the last few hours
    timeline = []
    for i in range(12):  # 12 time slots = last 12 hours
        timestamp = now - datetime.timedelta(hours=12 - i)
        timeline.append({
            "timestamp": timestamp.isoformat() + "Z",
            "errors": random.randint(0, 15)
        })

    # Mock pod performance
    pod_performance = {
        "inference-pod-1": {
            "timeouts": random.randint(0, 3),
            "ooms": random.randint(0, 2),
            "latency_avg_ms": random.randint(150, 400)
        },
        "inference-pod-2": {
            "timeouts": random.randint(0, 3),
            "ooms": random.randint(0, 1),
            "latency_avg_ms": random.randint(150, 400)
        }
    }

    # Mock auth/network anomalies
    auth_fails = random.randint(0, 10)
    network_timeouts = random.randint(0, 5)

    return {
        "severity_counts": severity_counts,
        "errors_by_component": errors_by_component,
        "timeline": timeline,
        "pod_performance": pod_performance,
        "auth_fails": auth_fails,
        "network_timeouts": network_timeouts
    }

