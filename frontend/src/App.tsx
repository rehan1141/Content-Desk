import { useState, useEffect } from "react";
import { Sparkles, Home, Inbox, Lightbulb, Compass, Youtube, Instagram, Linkedin, Settings, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";
import "./App.css";

interface HealthStatus {
  status: string;
  app: string;
  version: string;
  environment: string;
}

export function App() {
  const [activeNav, setActiveNav] = useState<string>("home");
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const checkBackendHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/api/v1/health");
      if (!res.ok) {
        throw new Error(`HTTP error ${res.status}`);
      }
      const data: HealthStatus = await res.json();
      setHealth(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to connect to backend");
      setHealth(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const navItems = [
    { id: "home", label: "Home", icon: Home },
    { id: "inbox", label: "Inbox", icon: Inbox },
    { id: "ideas", label: "Ideas", icon: Lightbulb },
    { id: "experiences", label: "Experiences", icon: Compass },
    { id: "youtube", label: "YouTube", icon: Youtube },
    { id: "instagram", label: "Instagram", icon: Instagram },
    { id: "linkedin", label: "LinkedIn", icon: Linkedin },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <div className="app-shell">
      {/* Sidebar Workspace Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">
            <Sparkles size={20} />
          </div>
          <div className="brand-info">
            <h1 className="brand-title">Content Desk</h1>
            <span className="brand-badge">V0.1 Dev</span>
          </div>
        </div>

        <nav className="nav-menu">
          {navItems.map((item) => {
            const IconComponent = item.icon;
            const isActive = activeNav === item.id;
            return (
              <button
                key={item.id}
                id={`nav-${item.id}`}
                className={`nav-item ${isActive ? "active" : ""}`}
                onClick={() => setActiveNav(item.id)}
              >
                <IconComponent size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <div className={`status-dot ${health ? "online" : "offline"}`} />
            <span className="status-label">
              {loading ? "Checking..." : health ? "Backend Online" : "Backend Offline"}
            </span>
          </div>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="main-content">
        <header className="workspace-header">
          <div className="header-title-container">
            <h2>{navItems.find((n) => n.id === activeNav)?.label || "Workspace"}</h2>
            <p className="header-subtitle">
              THOUGHT &rarr; IDEA &rarr; CONTENT &rarr; PUBLISH
            </p>
          </div>
        </header>

        <section className="workspace-body">
          <div className="card milestone-card">
            <div className="card-header">
              <h3>Milestone 1 — Application Shell & Backend Status</h3>
              <button className="icon-button" onClick={checkBackendHealth} title="Refresh connection">
                <RefreshCw size={16} className={loading ? "spin" : ""} />
              </button>
            </div>
            <div className="card-body">
              {loading ? (
                <div className="status-box loading">Connecting to FastAPI backend at port 8000...</div>
              ) : health ? (
                <div className="status-box success">
                  <CheckCircle2 size={22} className="text-success" />
                  <div>
                    <strong>FastAPI Backend Connected</strong>
                    <p>
                      App: <code>{health.app}</code> | Version: <code>{health.version}</code> | Env: <code>{health.environment}</code>
                    </p>
                  </div>
                </div>
              ) : (
                <div className="status-box error">
                  <AlertCircle size={22} className="text-error" />
                  <div>
                    <strong>Backend Not Connected</strong>
                    <p>{error || "Ensure backend server is running via uvicorn at http://localhost:8000"}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="card philosophy-card">
            <h4>Core Creative Philosophy</h4>
            <ul className="philosophy-list">
              <li><strong>Capture without friction:</strong> Fast, unconstrained thought entry.</li>
              <li><strong>Human creativity stays human:</strong> No fake AI script generation.</li>
              <li><strong>Lineage & Relationships:</strong> Ideas transform into multi-platform content.</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
