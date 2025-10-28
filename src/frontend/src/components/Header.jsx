import React from "react";
import "./Header.css";

export default function Header({ connected }) {
  return (
    <div className="header">
      <h2>⚡ LogPilot</h2>
      <div className={`status ${connected ? "online" : "offline"}`}>
        {connected ? "Connected" : "Offline"}
      </div>
    </div>
  );
}
