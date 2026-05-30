import type { InsightSeverity } from "@/lib/insights";

export function InsightSeverityBadge({ severity }: { severity: InsightSeverity }) {
  const label = severity === "negative" ? "Red flag" : severity === "positive" ? "Improvement" : severity === "warning" ? "Warning" : "Briefing";
  return <span className={`badge ${severity === "negative" ? "negative" : severity === "positive" ? "positive" : "neutral"}`}>{label}</span>;
}
