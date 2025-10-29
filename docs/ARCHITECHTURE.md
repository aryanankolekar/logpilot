# LogPilot Architecture Overview

This document outlines the high-level architecture of the LogPilot application, detailing the major components and the flow of data between them.

## High-Level Diagram

```
+-----------------+      +-----------------+      +-----------------+
|   Frontend      |      |   Backend API   |      |   Log Ingestion |
| (React/Vite)    | <--> | (FastAPI)       | <--> | (Python Watcher)|
+-----------------+      +-----------------+      +-----------------+
        |                      |                      |
        |                      |                      |
        v                      v                      v
+-----------------+      +-----------------+      +-----------------+
|   User          |      |   RAG Pipeline  |      |   Vector DB     |
| (Web Browser)   |      | (LLM/ChromaDB)  |      | (ChromaDB)      |
+-----------------+      +-----------------+      +-----------------+
```

## Component Breakdown

### 1. Frontend

- **Description**: A single-page application (SPA) built with **React** and **Vite**. It provides the user interface for displaying log data visualizations and interacting with the query system.
- **Responsibilities**:
  - Rendering the main dashboard, including charts and statistics from `react-chartjs-2`.
  - Providing an input interface for users to submit natural language queries.
  - Displaying the results returned from the backend in a clear and readable format.
  - Proxying API requests from the browser to the backend to avoid CORS issues.

### 2. Backend

- **Description**: A **FastAPI** application that serves as the central hub for the system. It exposes a RESTful API that the frontend consumes.
- **Responsibilities**:
  - Handling incoming HTTP requests from the frontend.
  - Serving aggregated log statistics for the visualization panel.
  - Orchestrating the Retrieval-Augmented Generation (RAG) pipeline to answer user queries.
  - Providing a health check endpoint to monitor the application's status.

### 3. Log Ingestion

- **Description**: A background thread initiated by the FastAPI application on startup. It uses a file system watcher to monitor a designated directory (`data/logs/`) for new or updated log files.
- **Responsibilities**:
  - Detecting changes to log files in real-time.
  - Reading new log entries and preprocessing them.
  - Generating sentence embeddings for each log entry using a `SentenceTransformer` model.
  - Storing the log entry and its corresponding embedding in the vector database (ChromaDB).
- **Key Point**: This process runs in a separate thread to avoid blocking the main FastAPI application and ensure the API remains responsive, especially during the initial, time-consuming model loading phase.

### 4. RAG (Retrieval-Augmented Generation) Pipeline

- **Description**: The core AI-powered component responsible for answering user queries. It combines a retrieval step with a generation step.
- **Flow**:
  1.  **Retrieval**: When a user submits a query, the backend generates an embedding for the query text. It then uses this embedding to search the **ChromaDB** vector store for the most semantically similar log entries.
  2.  **Augmentation**: The retrieved log entries (the "context") are combined with the original user query into a single prompt.
  3.  **Generation**: This combined prompt is then fed to a large language model (LLM), which generates a natural language answer based on the provided context.
- **Responsibilities**:
  - Understanding the user's query.
  - Finding relevant information within the log data.
  - Synthesizing an accurate and coherent answer.

### 5. Vector Database

- **Description**: **ChromaDB** is used as the vector store. It is responsible for efficiently storing and retrieving high-dimensional vector embeddings.
- **Responsibilities**:
  - Storing the embeddings of all processed log entries.
  - Performing efficient similarity searches to find log entries that are semantically related to a user's query.

## Data Flow

1.  **Log Ingestion**: The `ingest.py` script watches the `data/logs/` directory. When a new log file appears, it's read, parsed, and each line is converted into a vector embedding. These embeddings are stored in ChromaDB.
2.  **Frontend Visualization**: The React frontend periodically calls the `/api/stats` endpoint. The backend, using `log_utils.py`, aggregates the raw log data to compute statistics, which are returned to the frontend and displayed in the `VisualizationPanel`.
3.  **User Query**:
    - A user types a question into the `QueryInput` component in the frontend.
    - The query is sent to the backend's `/query` endpoint.
    - The `rag.py` module orchestrates the RAG pipeline: it retrieves relevant logs from ChromaDB, constructs a prompt, and sends it to the LLM.
    - The LLM's response is streamed back to the frontend and displayed in the `ResultsDisplay` component.

This architecture ensures a separation of concerns, allowing the frontend to focus on user interaction while the backend manages the complex data processing and AI-powered query resolution.
