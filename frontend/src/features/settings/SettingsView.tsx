import { Database, Sliders } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";

interface SettingsViewProps {
  isBackendConnected: boolean;
}

export function SettingsView({ isBackendConnected }: SettingsViewProps) {
  return (
    <div className="view-container">
      <div className="settings-grid">
        <Card className="settings-card">
          <div className="settings-card-header">
            <Database size={20} className="text-accent" />
            <div>
              <h5>Backend & Database</h5>
              <p>PostgreSQL connection & API settings</p>
            </div>
          </div>
          <div className="settings-item">
            <span>API Server</span>
            <code>http://localhost:8000/api/v1</code>
          </div>
          <div className="settings-item">
            <span>Database Status</span>
            <Badge variant={isBackendConnected ? "success" : "error"}>
              {isBackendConnected ? "PostgreSQL Active" : "Disconnected"}
            </Badge>
          </div>
        </Card>

        <Card className="settings-card">
          <div className="settings-card-header">
            <Sliders size={20} className="text-accent" />
            <div>
              <h5>Creator Workflow</h5>
              <p>Custom tags, flairs, and checklists</p>
            </div>
          </div>
          <div className="settings-item">
            <span>Default Flairs</span>
            <span>Opinion, Story, Educational, Hot Take</span>
          </div>
        </Card>
      </div>
    </div>
  );
}
