import React, { useState } from "react";

export default function InputBox({ onSend, disabled }) {
  const [text, setText] = useState("");

  const send = () => {
    if (text.trim()) {
      onSend(text.trim());
      setText("");
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="input-box">
      <textarea
        placeholder="Ask about logs…"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKey}
        disabled={disabled}
      />
      <button onClick={send} disabled={disabled}>
        ➤
      </button>
    </div>
  );
}
