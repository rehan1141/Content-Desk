import { Compass, Plus } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";

export function ExperiencesView() {
  return (
    <div className="view-container">
      <Card className="empty-state-card">
        <div className="empty-state-icon">
          <Compass size={32} />
        </div>
        <h4>Experiences Vault</h4>
        <p>
          Store real-life experiences, projects, mistakes, and lessons. Reuse them across YouTube scripts, LinkedIn posts, and Instagram reels.
        </p>
        <Button variant="primary" icon={<Plus size={16} />}>
          Add Experience
        </Button>
      </Card>
    </div>
  );
}
