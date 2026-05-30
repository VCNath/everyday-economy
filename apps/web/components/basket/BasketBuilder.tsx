import { Calculator } from "lucide-react";

import { BasketCostSummary } from "./BasketCostSummary";
import { BasketItemSelector } from "./BasketItemSelector";
import { BasketMethodology } from "./BasketMethodology";

export function BasketBuilder() {
  return (
    <section className="panel basket-builder">
      <div className="panel-header">
        <div>
          <p className="muted">Basket builder</p>
          <h2 className="section-title">Monthly essentials estimate</h2>
        </div>
        <button className="button primary" type="button">
          <Calculator size={16} aria-hidden />
          Calculate
        </button>
      </div>
      <BasketItemSelector />
      <BasketCostSummary />
      <BasketMethodology />
    </section>
  );
}
