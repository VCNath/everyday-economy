import { BasketBreakdownChart } from "@/components/charts/BasketBreakdownChart";

export function BasketDriversPanel() {
  return (
    <section className="panel">
      <p className="muted">Biggest drivers</p>
      <h2 className="section-title">Basket pressure mix</h2>
      <BasketBreakdownChart />
    </section>
  );
}
