import React from "react";

export default function Header({ onToggleSidebar }) {
  return (
    <header className="header">
      <button className="sidebar-toggle" onClick={onToggleSidebar}>
        ☰
      </button>
      <h1>LogPilot Copilot</h1>
      <div className="header-right">
        <button className="header-btn">⚙️</button>
      </div>
    </header>
  );
}
