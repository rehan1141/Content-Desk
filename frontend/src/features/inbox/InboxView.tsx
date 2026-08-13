import { Inbox, Plus } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";

interface InboxViewProps {
  onQuickCapture: () => void;
}

export function InboxView({ onQuickCapture }: InboxViewProps) {
  return (
    <div className="view-container">
      <Card className="empty-state-card">
        <div className="empty-state-icon">
          <Inbox size={32} />
        </div>
        <h4>Your Inbox is empty</h4>
        <p>
          Capture random thoughts, observations, and raw ideas instantly. No titles, tags, or deadlines required.
        </p>
        <Button variant="primary" icon={<Plus size={16} />} onClick={onQuickCapture}>
          Capture First Thought
        </Button>
      </Card>
    </div>
  );
}
