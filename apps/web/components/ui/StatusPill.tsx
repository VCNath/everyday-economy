import { Chip } from "@mui/material";

export function StatusPill({
  label,
  tone = "neutral",
}: {
  label: string;
  tone?: "positive" | "negative" | "warning" | "neutral" | "info";
}) {
  return <Chip className={`status-pill ${tone}`} label={label} size="small" />;
}
