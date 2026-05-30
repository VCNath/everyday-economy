import { formatMetric } from "@/lib/formatters";
import type { RegionSummary } from "@/lib/types";
import { FreshnessBadge } from "@/components/data/FreshnessBadge";

export function RegionSummaryCard({ summary }: { summary: RegionSummary }) {
  return (
    <section className="panel region-summary">
      <div>
        <p className="muted">Selected region</p>
        <h2>{summary.name}</h2>
        <FreshnessBadge status="healthy" />
        <p>{summary.insight}</p>
      </div>
      <dl className="summary-metrics">
        <div>
          <dt>Overall inflation</dt>
          <dd>{formatMetric(summary.metrics.cpi_all_items_yoy, "%")}</dd>
        </div>
        <div>
          <dt>Food inflation</dt>
          <dd>{formatMetric(summary.metrics.cpi_food_yoy, "%")}</dd>
        </div>
        <div>
          <dt>Gasoline</dt>
          <dd>{summary.metrics.gas_regular_cents_litre.toFixed(1)}c/L</dd>
        </div>
        <div>
          <dt>Unemployment</dt>
          <dd>{formatMetric(summary.metrics.unemployment_rate, "%")}</dd>
        </div>
        <div>
          <dt>Basic basket</dt>
          <dd>{formatMetric(summary.metrics.basic_basket_monthly_cost, "CAD/month")}</dd>
        </div>
        <div>
          <dt>Affordability</dt>
          <dd>{formatMetric(summary.metrics.affordability_score, "score")}</dd>
        </div>
      </dl>
    </section>
  );
}
