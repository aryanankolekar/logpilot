import React from "react";
import ReactMarkdown from "react-markdown";
import "./ChatContainer.css";

export default function ChatContainer({ messages }) {
  return (
    <div className="chat-container">
      {messages.map((msg, idx) => (
        <div key={idx} className={`message ${msg.role}`}>
          <div className="bubble">
            {msg.role === "assistant" ? (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            ) : (
              msg.text
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
