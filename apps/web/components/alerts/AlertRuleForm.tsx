"use client";

import { useState } from "react";

import type { AlertRuleCreatePayload } from "@/lib/types";

export function AlertRuleForm({ locationId, onSubmit }: { locationId?: string; onSubmit: (payload: AlertRuleCreatePayload) => Promise<void> }) {
  const [location, setLocation] = useState(locationId ?? "CA-SK");
  const [indicator, setIndicator] = useState("cpi_food_yoy");
  const [operator, setOperator] = useState("gte");
  const [threshold, setThreshold] = useState("5");
  const [submitting, setSubmitting] = useState(false);

  async function submit() {
    setSubmitting(true);
    try {
      await onSubmit({
        location_id: location,
        indicator_id: indicator,
        alert_type: "threshold",
        comparison_operator: operator,
        threshold_value: Number(threshold),
        channel_in_app: true,
        channel_email: false,
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="panel preference-grid">
      <label className="field"><span>Region</span><input value={location} onChange={(e) => setLocation(e.target.value)} /></label>
      <label className="field"><span>Metric</span>
        <select value={indicator} onChange={(e) => setIndicator(e.target.value)}>
          <option value="cpi_all_items_yoy">Overall inflation</option>
          <option value="cpi_food_yoy">Food inflation</option>
          <option value="cpi_shelter_yoy">Shelter inflation</option>
          <option value="gas_regular_cents_litre">Gas price</option>
          <option value="unemployment_rate">Unemployment</option>
          <option value="basic_basket_monthly_cost">Basic basket cost</option>
          <option value="affordability_score">Affordability score</option>
        </select>
      </label>
      <label className="field"><span>Operator</span>
        <select value={operator} onChange={(e) => setOperator(e.target.value)}>
          <option value="gt">Greater than</option>
          <option value="gte">Greater than or equal</option>
          <option value="lt">Less than</option>
          <option value="lte">Less than or equal</option>
        </select>
      </label>
      <label className="field"><span>Threshold</span><input value={threshold} onChange={(e) => setThreshold(e.target.value)} type="number" /></label>
      <button className="button primary" type="button" disabled={submitting} onClick={submit}>{submitting ? "Creating..." : "Create alert"}</button>
    </section>
  );
}

