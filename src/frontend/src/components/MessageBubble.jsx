import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function MessageBubble({ role, text }) {
  const isUser = role === "user";
  return (
    <div className={`msg-bubble ${isUser ? "user" : "assistant"}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
    </div>
  );
}
