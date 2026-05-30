"use client";

import { Moon, Sun } from "lucide-react";
import { useThemeMode } from "@/components/theme/AppThemeProvider";

export function ThemeToggle() {
  const { mode, toggleMode } = useThemeMode();
  const Icon = mode === "dark" ? Sun : Moon;
  return (
    <button className="icon-button" type="button" aria-label={`Switch to ${mode === "dark" ? "light" : "dark"} theme`} onClick={toggleMode}>
      <Icon size={17} aria-hidden />
    </button>
  );
}
