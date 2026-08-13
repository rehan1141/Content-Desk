import { Lightbulb, Plus } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";

export function IdeasView() {
  return (
    <div className="view-container">
      <Card className="empty-state-card">
        <div className="empty-state-icon">
          <Lightbulb size={32} />
        </div>
        <h4>Ideas Workspace</h4>
        <p>
          Develop raw thoughts into structured content concepts. Track status from RAW &rarr; DEVELOPING &rarr; DRAFT &rarr; READY.
        </p>
        <Button variant="primary" icon={<Plus size={16} />}>
          Create New Idea
        </Button>
      </Card>
    </div>
  );
}
