"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

type ThemeMode = "light" | "dark";

const ThemeModeContext = createContext<{
  mode: ThemeMode;
  setMode: (mode: ThemeMode) => void;
  toggleMode: () => void;
} | null>(null);

function buildTheme(mode: ThemeMode) {
  const isDark = mode === "dark";
  return createTheme({
    palette: {
      mode,
      primary: { main: "#2563EB", dark: "#1D4ED8", light: "#DBEAFE" },
      secondary: { main: "#38BDF8", light: "#E0F2FE" },
      success: { main: "#22C55E", dark: "#16A34A", light: "#DCFCE7" },
      warning: { main: "#F59E0B" },
      error: { main: "#EF4444" },
      background: {
        default: isDark ? "#07111F" : "#F8FBFF",
        paper: isDark ? "rgba(15, 23, 42, 0.78)" : "rgba(255, 255, 255, 0.78)",
      },
      text: {
        primary: isDark ? "#F8FAFC" : "#0F172A",
        secondary: isDark ? "#CBD5E1" : "#475569",
      },
    },
    shape: { borderRadius: 12 },
    typography: {
      fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      h1: { fontWeight: 850, letterSpacing: 0 },
      h2: { fontWeight: 800, letterSpacing: 0 },
      h3: { fontWeight: 750, letterSpacing: 0 },
      button: { textTransform: "none", fontWeight: 750 },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
            border: isDark ? "1px solid rgba(148, 163, 184, 0.18)" : "1px solid rgba(37, 99, 235, 0.12)",
            backdropFilter: "blur(20px)",
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 10,
            boxShadow: "none",
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            fontWeight: 700,
          },
        },
      },
    },
  });
}

export function AppThemeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setModeState] = useState<ThemeMode>("light");

  useEffect(() => {
    const saved = window.localStorage.getItem("ee_theme") as ThemeMode | null;
    const preferred = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    setModeState(saved === "dark" || saved === "light" ? saved : preferred);
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = mode;
  }, [mode]);

  const value = useMemo(
    () => ({
      mode,
      setMode(next: ThemeMode) {
        window.localStorage.setItem("ee_theme", next);
        setModeState(next);
      },
      toggleMode() {
        const next = mode === "dark" ? "light" : "dark";
        window.localStorage.setItem("ee_theme", next);
        setModeState(next);
      },
    }),
    [mode]
  );
  const theme = useMemo(() => buildTheme(mode), [mode]);

  return (
    <ThemeModeContext.Provider value={value}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeModeContext.Provider>
  );
}

export function useThemeMode() {
  const value = useContext(ThemeModeContext);
  if (!value) {
    throw new Error("useThemeMode must be used inside AppThemeProvider.");
  }
  return value;
}
