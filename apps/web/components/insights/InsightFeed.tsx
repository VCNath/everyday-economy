import { InsightCard } from "./InsightCard";
import type { InsightItem } from "@/lib/insights";

export function InsightFeed({ insights }: { insights: InsightItem[] }) {
  return (
    <div className="insight-feed">
      {insights.map((insight) => (
        <InsightCard
          key={insight.id}
          severity={insight.severity}
          title={insight.title}
          body={insight.body}
          source={insight.source}
          period={insight.period}
        />
      ))}
    </div>
  );
}
