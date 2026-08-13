import React from "react";
import "./ui.css";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export function Card({ children, className = "", onClick, hoverable = false }: CardProps) {
  return (
    <div
      className={`ui-card ${hoverable ? "hoverable" : ""} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
