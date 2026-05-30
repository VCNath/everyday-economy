import { BasketBreakdownChart } from "@/components/charts/BasketBreakdownChart";

export function RegionBasketBreakdown() {
  return (
    <section className="panel">
      <h2 className="section-title">Basket cost breakdown</h2>
      <BasketBreakdownChart />
    </section>
  );
}
