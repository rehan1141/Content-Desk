import React from "react";
import "./ui.css";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "accent" | "success" | "warning" | "error" | "outline";
  size?: "sm" | "md";
  className?: string;
}

export function Badge({ children, variant = "default", size = "sm", className = "" }: BadgeProps) {
  return (
    <span className={`ui-badge badge-${variant} badge-${size} ${className}`}>
      {children}
    </span>
  );
}
