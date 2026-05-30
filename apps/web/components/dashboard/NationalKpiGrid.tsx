import { MetricCard } from "@/components/cards/MetricCard";

export function NationalKpiGrid() {
  return (
    <section className="kpi-grid">
      <MetricCard label="CPI" value="2.7%" helper="Overall consumer prices" trend={2.7} tone="warning" />
      <MetricCard label="Food" value="3.9%" helper="Grocery and restaurant prices" trend={3.9} tone="negative" />
      <MetricCard label="Gas" value="158.6c/L" helper="Cost to commute or drive" tone="warning" />
      <MetricCard label="Jobs" value="6.1%" helper="Unemployment rate" tone="neutral" />
      <MetricCard label="Best region" value="Manitoba" helper="Highest affordability score" tone="positive" />
      <MetricCard label="Worst region" value="Nunavut" helper="Lowest affordability score" tone="negative" />
    </section>
  );
}
