import React from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function Sidebar({ open, conversations, activeChat, onSelect }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.aside
          className="sidebar"
          initial={{ x: -200, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -200, opacity: 0 }}
        >
          <h3>Conversations</h3>
          <div className="chat-list">
            {conversations.length === 0 && (
              <p className="empty">No chats yet</p>
            )}
            {conversations.map((c, i) => (
              <div
                key={i}
                className={`chat-item ${activeChat === i ? "active" : ""}`}
                onClick={() => onSelect(i)}
              >
                {c.title || `Chat ${i + 1}`}
              </div>
            ))}
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
