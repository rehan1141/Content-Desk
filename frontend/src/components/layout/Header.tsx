import { Plus, Search, Command } from "lucide-react";
import { Button } from "../ui/Button";
import "./layout.css";

interface HeaderProps {
  title: string;
  subtitle?: string;
  onQuickCapture?: () => void;
}

export function Header({ title, subtitle, onQuickCapture }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="header-left">
        <h2 className="header-title">{title}</h2>
        {subtitle && <p className="header-subtitle">{subtitle}</p>}
      </div>

      <div className="header-actions">
        <div className="search-bar-placeholder">
          <Search size={16} className="search-icon" />
          <input
            type="text"
            placeholder="Search thoughts, ideas, experiences..."
            className="header-search-input"
            readOnly
          />
          <kbd className="keyboard-shortcut"><Command size={11} /> K</kbd>
        </div>

        <Button variant="primary" icon={<Plus size={16} />} onClick={onQuickCapture}>
          Quick Capture
        </Button>
      </div>
    </header>
  );
}
