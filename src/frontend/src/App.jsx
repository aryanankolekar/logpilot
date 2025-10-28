import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newMessage = { role: "user", content: query };
    setMessages((prev) => [...prev, newMessage]);
    setQuery("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:6969/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      const reply = {
        role: "assistant",
        content: data.answer || "No answer generated.",
      };

      setMessages((prev) => [...prev, reply]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Server took too long to respond or is offline.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Chat Section */}
      <div className="chat-section">
        <div className="chat-header">LogPilot - Query Your Logs</div>
        <div className="chat-window">
          {messages.map((msg, i) => (
            <div key={i} className={`msg ${msg.role}`}>
              <div className="msg-text">{msg.content}</div>
            </div>
          ))}
          {loading && <div className="msg assistant">Analyzing logs...</div>}
        </div>

        <form onSubmit={sendQuery} className="chat-input-area">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask something about your logs..."
          />
          <button type="submit" disabled={loading}>
            {loading ? "..." : "Send"}
          </button>
        </form>
      </div>

      {/* Visualization Section */}
      <div className="viz-section">
        <div className="viz-header">Log Insights</div>
        <div className="viz-body">
          <p>Visualizations will appear here dynamically.</p>
          <p className="placeholder">
            Real-time charts, error trends, pod metrics, etc.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
