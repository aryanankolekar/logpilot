import React, { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import VisualizationPanel from "./components/VisualizationPanel";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  return (
    <div className="app-wrapper">
      <Header onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />

      <div className="main-layout">
        <Sidebar
          open={sidebarOpen}
          conversations={conversations}
          activeChat={activeChat}
          onSelect={(chat) => setActiveChat(chat)}
        />

        <ChatArea
          activeChat={activeChat}
          setConversations={setConversations}
          conversations={conversations}
        />

        <VisualizationPanel />
      </div>
    </div>
  );
}
