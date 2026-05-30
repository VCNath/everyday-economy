import { MetricCard } from "@/components/cards/MetricCard";
import type { CompareMetricRow } from "@/lib/types";

export function CompareKpiGrid({
  rows,
  metricLabel
}: {
  rows: CompareMetricRow[];
  metricLabel: string;
}) {
  return (
    <section className="kpi-grid three">
      {rows.map((row) => (
        <MetricCard
          key={row.location_id}
          label={row.location_name}
          value={row.value !== null ? `${row.value.toFixed(1)} ${row.unit}` : "—"}
          helper={row.trust.is_estimated ? `${metricLabel} · Estimated` : `${metricLabel} · ${row.trust.source_name ?? "Unknown source"}`}
          tone="neutral"
        />
      ))}
    </section>
  );
}
