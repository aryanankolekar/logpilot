# LogPilot Frontend

This directory contains the frontend for the LogPilot application, an interactive web interface for visualizing and querying log data.

## Overview

The frontend is a single-page application (SPA) built with React. It communicates with the backend API to:

- Display real-time log statistics on an interactive dashboard.
- Allow users to submit natural language queries.
- Render query results in a user-friendly format.

## Tech Stack

- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Standard CSS with some components using inline styles.
- **Data Visualization**: `react-chartjs-2`
- **API Communication**: `axios` (via a wrapper in `src/api.js`)

## Getting Started

### Prerequisites

- Node.js 14+
- npm

### Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd src/frontend
    ```

2.  **Install npm dependencies:**

    ```bash
    npm install
    ```

3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`. The Vite development server is configured to proxy API requests to the backend running on `http://localhost:8000`.

## Project Structure

```
frontend/
├── public/              # Static assets
└── src/
    ├── components/      # Reusable React components
    │   ├── QueryInput.jsx
    │   ├── ResultsDisplay.jsx
    │   └── VisualizationPanel.jsx
    ├── App.jsx          # Main application component, manages layout and state.
    ├── main.jsx         # Application entry point.
    ├── api.js           # Wrapper for making API calls to the backend.
    └── styles.css       # Global styles.
```
