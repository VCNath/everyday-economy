import { DataCoverageBadge } from "@/components/data/DataCoverageBadge";
import { EstimatedBadge } from "@/components/data/EstimatedBadge";

export function BasketSummaryCard() {
  return (
    <section className="panel basket-summary-card">
      <p className="muted">Basket summary</p>
      <strong>$428/mo</strong>
      <span className="trust-badges"><EstimatedBadge show={true} /> <DataCoverageBadge coverageScore={0.82} /></span>
      <span>+3.7% year over year</span>
      <p>Biggest drivers: protein, dairy, and produce.</p>
    </section>
  );
}
