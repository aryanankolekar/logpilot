import React, { useState } from "react";
import "./InputBar.css";

export default function InputBar({ onSend, loading }) {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    if (!query.trim() || loading) return;
    onSend(query.trim());
    setQuery("");
  };

  return (
    <div className="input-bar">
      <input
        type="text"
        placeholder="Ask LogPilot anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}
