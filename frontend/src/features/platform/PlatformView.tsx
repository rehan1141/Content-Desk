import { Youtube, Instagram, Linkedin, Plus } from "lucide-react";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";

interface PlatformViewProps {
  platform: "youtube" | "instagram" | "linkedin";
}

export function PlatformView({ platform }: PlatformViewProps) {
  const platformConfig = {
    youtube: {
      name: "YouTube Workspace",
      icon: Youtube,
      badge: "YouTube",
      badgeVariant: "error" as const,
      formats: ["Long-form Videos", "Shorts"],
      description: "Manage scripts, video outlines, recording checklists, and repurposed clips.",
    },
    instagram: {
      name: "Instagram Workspace",
      icon: Instagram,
      badge: "Instagram",
      badgeVariant: "warning" as const,
      formats: ["Reels", "Carousels", "Stories"],
      description: "Manage visual hooks, reel scripts, carousel slide outlines, and captions.",
    },
    linkedin: {
      name: "LinkedIn Workspace",
      icon: Linkedin,
      badge: "LinkedIn",
      badgeVariant: "accent" as const,
      formats: ["Text Posts", "PDF Documents"],
      description: "Manage thought-leadership posts, breakdowns, and professional reflections.",
    },
  };

  const config = platformConfig[platform];
  const Icon = config.icon;

  return (
    <div className="view-container">
      <div className="platform-header-banner">
        <Badge variant={config.badgeVariant} size="md">
          <Icon size={14} />
          <span>{config.badge}</span>
        </Badge>
        <h3>{config.name}</h3>
        <p>{config.description}</p>

        <div className="format-tags">
          {config.formats.map((fmt) => (
            <Badge key={fmt} variant="outline">
              {fmt}
            </Badge>
          ))}
        </div>
      </div>

      <Card className="empty-state-card">
        <div className="empty-state-icon">
          <Icon size={32} />
        </div>
        <h4>No content drafted yet</h4>
        <p>Convert ideas into {config.name} drafts when ready.</p>
        <Button variant="primary" icon={<Plus size={16} />}>
          Draft New {config.badge} Content
        </Button>
      </Card>
    </div>
  );
}
