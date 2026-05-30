import { InsightSeverityBadge } from "./InsightSeverityBadge";
import { InsightSourceLinks } from "./InsightSourceLinks";
import type { InsightSeverity } from "@/lib/insights";

export function InsightCard({
  severity,
  title,
  body,
  source,
  period
}: {
  severity: InsightSeverity;
  title: string;
  body: string;
  source: string;
  period: string;
}) {
  return (
    <article className="panel insight-feed-card">
      <InsightSeverityBadge severity={severity} />
      <h2>{title}</h2>
      <p>{body}</p>
      <InsightSourceLinks source={source} period={period} />
    </article>
  );
}
