import { useState, useEffect } from "react";
import { Sidebar, NavTab } from "./components/layout/Sidebar";
import { Header } from "./components/layout/Header";
import { HomeView } from "./features/home/HomeView";
import { InboxView } from "./features/inbox/InboxView";
import { IdeasView } from "./features/ideas/IdeasView";
import { ExperiencesView } from "./features/experiences/ExperiencesView";
import { PlatformView } from "./features/platform/PlatformView";
import { SettingsView } from "./features/settings/SettingsView";
import "./App.css";
import "./features/views.css";

export function App() {
  const [activeTab, setActiveTab] = useState<NavTab>("home");
  const [isBackendConnected, setIsBackendConnected] = useState<boolean>(false);

  const checkBackendHealth = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/health");
      if (res.ok) {
        setIsBackendConnected(true);
      } else {
        setIsBackendConnected(false);
      }
    } catch {
      setIsBackendConnected(false);
    }
  };

  useEffect(() => {
    checkBackendHealth();
    const interval = setInterval(checkBackendHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleQuickCaptureTrigger = () => {
    setActiveTab("inbox");
  };

  const getHeaderMeta = (): { title: string; subtitle?: string } => {
    switch (activeTab) {
      case "home":
        return {
          title: "Home Workspace",
          subtitle: "THOUGHT → IDEA → CONTENT → PUBLISH",
        };
      case "inbox":
        return {
          title: "Inbox",
          subtitle: "Frictionless capture for raw thoughts & observations",
        };
      case "ideas":
        return {
          title: "Ideas",
          subtitle: "Lifecycle: RAW → DEVELOPING → DRAFT → READY",
        };
      case "experiences":
        return {
          title: "Experiences",
          subtitle: "Reusable personal brand stories, lessons, and project milestones",
        };
      case "youtube":
        return {
          title: "YouTube Workspace",
          subtitle: "Long-form video scripts & YouTube Shorts",
        };
      case "instagram":
        return {
          title: "Instagram Workspace",
          subtitle: "Reels, Carousel outlines, & Captions",
        };
      case "linkedin":
        return {
          title: "LinkedIn Workspace",
          subtitle: "Thought leadership posts & Document carousels",
        };
      case "settings":
        return {
          title: "Settings & System",
          subtitle: "API status, configuration, and preferences",
        };
      default:
        return { title: "Content Desk" };
    }
  };

  const renderActiveView = () => {
    switch (activeTab) {
      case "home":
        return <HomeView onNavigate={setActiveTab} onQuickCapture={handleQuickCaptureTrigger} />;
      case "inbox":
        return <InboxView onQuickCapture={handleQuickCaptureTrigger} />;
      case "ideas":
        return <IdeasView />;
      case "experiences":
        return <ExperiencesView />;
      case "youtube":
        return <PlatformView platform="youtube" />;
      case "instagram":
        return <PlatformView platform="instagram" />;
      case "linkedin":
        return <PlatformView platform="linkedin" />;
      case "settings":
        return <SettingsView isBackendConnected={isBackendConnected} />;
      default:
        return <HomeView onNavigate={setActiveTab} onQuickCapture={handleQuickCaptureTrigger} />;
    }
  };

  const headerMeta = getHeaderMeta();

  return (
    <div className="app-shell">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        isBackendConnected={isBackendConnected}
      />

      {/* Main Content Workspace */}
      <div className="main-layout">
        <Header
          title={headerMeta.title}
          subtitle={headerMeta.subtitle}
          onQuickCapture={handleQuickCaptureTrigger}
        />
        <main className="view-content-area">{renderActiveView()}</main>
      </div>
    </div>
  );
}

export default App;
