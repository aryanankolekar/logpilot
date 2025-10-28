# LogPilot

LogPilot is a powerful, AI-powered log analysis and visualization tool designed to help developers and system administrators effortlessly monitor and query application logs. It combines a robust FastAPI backend with a user-friendly React frontend to provide a seamless log exploration experience.

## Features

- **Real-time Log Monitoring**: Automatically watches for and processes new log entries.
- **AI-Powered Querying**: Utilizes natural language processing to answer complex queries about your logs.
- **Interactive Dashboard**: Visualizes log statistics for at-a-glance insights.
- **RESTful API**: Provides a well-defined API for querying and retrieving log data.

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: React, Vite, Chart.js
- **Language**: Python, JavaScript

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm

### Backend Setup

1. **Clone the repository:**
   ```bash
   # Clone the repository and navigate to the project directory
   git clone <repository-url>
   cd logpilot
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server:**
   ```bash
   uvicorn src.backend.app.main:app --host 127.0.0.1 --port 8000
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd src/frontend
   ```

2. **Install npm dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```

## Usage

Once the frontend and backend servers are running, you can access the application in your browser at `http://localhost:5173`.

### API Endpoints

- **POST /query**: Submit a natural language query about your logs.
- **GET /api/stats**: Retrieve aggregated log statistics for visualization.

## Project Structure

```
logpilot/
├── src/
│   ├── backend/
│   │   └── app/
│   │       ├── main.py        # FastAPI application
│   │       ├── rag.py         # RAG implementation
│   │       └── ...
│   └── frontend/
│       └── src/
│           ├── components/    # React components
│           ├── App.jsx        # Main application component
│           └── ...
├── data/
│   └── logs/                  # Log files
└── README.md
```
