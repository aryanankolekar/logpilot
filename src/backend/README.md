# LogPilot Backend

This directory contains the backend for the LogPilot application, a powerful, AI-powered log analysis and visualization tool.

## Overview

The backend is a FastAPI application responsible for:

- Ingesting and processing log files in real-time.
- Providing a RESTful API for querying log data using natural language.
- Serving aggregated log statistics for frontend visualization.
- Handling the embedding and retrieval of log data for the RAG model.

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Data Handling**: Pydantic
- **AI/ML**: SentenceTransformers, ChromaDB

## Getting Started

### Prerequisites

- Python 3.8+

### Setup

1.  **Navigate to the project root directory.**

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the backend server:**
    ```bash
    uvicorn src.backend.app.main:app --host 127.0.0.1 --port 8000
    ```
    The server will be accessible at `http://127.0.0.1:8000`.

## Project Structure

```
backend/
└── app/
    ├── main.py        # FastAPI application entry point, defines API endpoints.
    ├── rag.py         # Handles the Retrieval-Augmented Generation logic for answering queries.
    ├── ingest.py      # Manages real-time log ingestion and processing.
    ├── log_utils.py   # Provides utility functions for log aggregation and statistics.
    ├── embeddings.py  # Manages the creation of sentence embeddings for logs.
    ├── storage.py     # Handles the vector storage and retrieval (ChromaDB).
    ├── llm.py         # Interface for the language model.
    └── config.py      # Application configuration settings.
```

## API Endpoints

- **`POST /query`**: Accepts a JSON payload with a "query" key to submit a natural language question about the logs.
- **`GET /api/stats`**: Returns aggregated log statistics, such as severity counts and trends, for the visualization panel.
- **`GET /health`**: A health check endpoint that returns the status of the application, including whether the embedding model is ready.
