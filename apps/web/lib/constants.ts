import type { MetricKey } from "./types";

export const metricOptions: Array<{ id: MetricKey; label: string; unit: string }> = [
  { id: "cpi_all_items_yoy", label: "CPI", unit: "%" },
  { id: "cpi_food_yoy", label: "Food CPI", unit: "%" },
  { id: "basic_basket_monthly_cost", label: "Grocery Basket", unit: "$/mo" },
  { id: "gas_regular_cents_litre", label: "Gas", unit: "c/L" },
  { id: "unemployment_rate", label: "Unemployment", unit: "%" },
  { id: "affordability_score", label: "Affordability", unit: "/100" }
];

export const metricTranslation: Record<MetricKey, string> = {
  cpi_all_items_index: "Overall consumer price index",
  cpi_all_items_yoy: "Overall consumer prices",
  cpi_food_index: "Food consumer price index",
  cpi_food_yoy: "Grocery and restaurant price pressure",
  cpi_shelter_index: "Shelter consumer price index",
  cpi_shelter_yoy: "Rent, mortgage interest, utilities, and housing pressure",
  gas_regular_cents_litre: "Cost to commute or drive",
  unemployment_rate: "Job market softness",
  employment_rate: "Share of working-age people employed",
  participation_rate: "Share of working-age people in the labour force",
  basic_basket_monthly_cost: "Estimated monthly cost of selected essentials",
  basic_basket_yoy: "Year-over-year change in the basic basket",
  affordability_score: "Household pressure score",
  boc_policy_rate: "Bank of Canada policy-rate context",
  cad_usd_exchange_rate: "Canadian dollar per U.S. dollar"
};
