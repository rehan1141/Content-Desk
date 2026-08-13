import { Lightbulb, Inbox, Compass, ArrowRight, Zap } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { NavTab } from "../../components/layout/Sidebar";

interface HomeViewProps {
  onNavigate: (tab: NavTab) => void;
  onQuickCapture: () => void;
}

export function HomeView({ onNavigate, onQuickCapture }: HomeViewProps) {
  const statCards = [
    { label: "Inbox Thoughts", value: "0", tab: "inbox" as NavTab, icon: Inbox, badge: "Raw Capture" },
    { label: "Active Ideas", value: "0", tab: "ideas" as NavTab, icon: Lightbulb, badge: "Developing" },
    { label: "Experiences", value: "0", tab: "experiences" as NavTab, icon: Compass, badge: "Reusable Atoms" },
  ];

  return (
    <div className="view-container">
      {/* Quick Action Hero Banner */}
      <Card className="hero-card">
        <div className="hero-content">
          <div className="hero-badge">
            <Zap size={14} />
            <span>Human-First Creative Loop</span>
          </div>
          <h3>What are you thinking about right now?</h3>
          <p>
            Capture your raw thoughts in seconds without title, platform, or tagging friction.
          </p>
          <div className="hero-actions">
            <Button variant="primary" onClick={onQuickCapture}>
              New Quick Capture
            </Button>
            <Button variant="outline" onClick={() => onNavigate("ideas")}>
              Explore Ideas Workspace
            </Button>
          </div>
        </div>
      </Card>

      {/* Metrics & Shortcuts */}
      <div className="stats-grid">
        {statCards.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card
              key={stat.label}
              hoverable
              onClick={() => onNavigate(stat.tab)}
              className="stat-card"
            >
              <div className="stat-header">
                <div className="stat-icon-wrapper">
                  <Icon size={20} />
                </div>
                <Badge variant="accent">{stat.badge}</Badge>
              </div>
              <div className="stat-body">
                <span className="stat-value">{stat.value}</span>
                <span className="stat-label">{stat.label}</span>
              </div>
              <div className="stat-footer">
                <span>View workspace</span>
                <ArrowRight size={14} />
              </div>
            </Card>
          );
        })}
      </div>

      {/* Platform Breakdown Overview */}
      <div className="workspace-section">
        <div className="section-header">
          <h4>Platform Spaces</h4>
          <span className="section-subtitle">Dedicated spaces for multi-format content</span>
        </div>

        <div className="platforms-grid">
          <Card hoverable onClick={() => onNavigate("youtube")} className="platform-card">
            <Badge variant="error" size="sm">YouTube</Badge>
            <h5>Long-form & Shorts</h5>
            <p>Scripts, video outlines, recording checklists, and repurposed shorts.</p>
          </Card>

          <Card hoverable onClick={() => onNavigate("instagram")} className="platform-card">
            <Badge variant="warning" size="sm">Instagram</Badge>
            <h5>Reels & Carousels</h5>
            <p>Visual hooks, carousel slide outlines, and caption drafts.</p>
          </Card>

          <Card hoverable onClick={() => onNavigate("linkedin")} className="platform-card">
            <Badge variant="accent" size="sm">LinkedIn</Badge>
            <h5>Posts & Documents</h5>
            <p>Thought leadership posts, breakdown carousels, and reflections.</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
