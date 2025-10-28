import React, { useState, useRef, useEffect } from "react";
import { sendQuery } from "../api";
import MessageBubble from "./MessageBubble";
import InputBox from "./InputBox";

export default function ChatArea({
  activeChat,
  setConversations,
  conversations,
}) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatRef = useRef();

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [messages]);

  async function handleSend(text) {
    if (!text.trim()) return;

    const userMsg = { role: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendQuery(text);
      const aiMsg = { role: "assistant", text: res.answer || "No response." };
      setMessages((prev) => [...prev, aiMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Error contacting backend." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-area">
      <div className="chat-content" ref={chatRef}>
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} text={m.text} />
        ))}
        {loading && <div className="loading">...</div>}
      </div>
      <InputBox onSend={handleSend} disabled={loading} />
    </div>
  );
}
