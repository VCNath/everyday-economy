import { Paper } from "@mui/material";

export function GlassCard({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <Paper className={`glass-card ${className}`} elevation={0}>
      {children}
    </Paper>
  );
}
