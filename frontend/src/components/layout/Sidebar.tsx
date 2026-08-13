import React from "react";
import { Sparkles, Home, Inbox, Lightbulb, Compass, Youtube, Instagram, Linkedin, Settings } from "lucide-react";
import "./layout.css";

export type NavTab = "home" | "inbox" | "ideas" | "experiences" | "youtube" | "instagram" | "linkedin" | "settings";

interface SidebarProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  isBackendConnected: boolean;
}

export function Sidebar({ activeTab, onTabChange, isBackendConnected }: SidebarProps) {
  const mainNavItems: { id: NavTab; label: string; icon: React.ElementType }[] = [
    { id: "home", label: "Home", icon: Home },
    { id: "inbox", label: "Inbox", icon: Inbox },
    { id: "ideas", label: "Ideas", icon: Lightbulb },
    { id: "experiences", label: "Experiences", icon: Compass },
  ];

  const platformNavItems: { id: NavTab; label: string; icon: React.ElementType }[] = [
    { id: "youtube", label: "YouTube", icon: Youtube },
    { id: "instagram", label: "Instagram", icon: Instagram },
    { id: "linkedin", label: "LinkedIn", icon: Linkedin },
  ];

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <Sparkles size={20} />
        </div>
        <div className="brand-meta">
          <h1 className="brand-name">Content Desk</h1>
          <span className="brand-version">V0.1</span>
        </div>
      </div>

      <div className="sidebar-section">
        <span className="section-title">CORE</span>
        <nav className="sidebar-nav">
          {mainNavItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                id={`nav-${item.id}`}
                className={`nav-button ${isActive ? "active" : ""}`}
                onClick={() => onTabChange(item.id)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-section">
        <span className="section-title">PLATFORMS</span>
        <nav className="sidebar-nav">
          {platformNavItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                id={`nav-${item.id}`}
                className={`nav-button ${isActive ? "active" : ""}`}
                onClick={() => onTabChange(item.id)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <button
          id="nav-settings"
          className={`nav-button ${activeTab === "settings" ? "active" : ""}`}
          onClick={() => onTabChange("settings")}
        >
          <Settings size={18} />
          <span>Settings</span>
        </button>

        <div className="backend-indicator">
          <div className={`indicator-dot ${isBackendConnected ? "online" : "offline"}`} />
          <span className="indicator-text">
            {isBackendConnected ? "Backend Connected" : "Backend Offline"}
          </span>
        </div>
      </div>
    </aside>
  );
}
