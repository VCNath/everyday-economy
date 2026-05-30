import type { MetricKey } from "./types";

export const indicatorLabels: Record<MetricKey, string> = {
  cpi_all_items_index: "All-items CPI index",
  cpi_all_items_yoy: "Overall inflation",
  cpi_food_index: "Food CPI index",
  cpi_food_yoy: "Food pressure",
  cpi_shelter_index: "Shelter CPI index",
  cpi_shelter_yoy: "Shelter pressure",
  gas_regular_cents_litre: "Gas prices",
  unemployment_rate: "Unemployment",
  employment_rate: "Employment rate",
  participation_rate: "Participation rate",
  basic_basket_monthly_cost: "Grocery basket",
  basic_basket_yoy: "Grocery basket YoY",
  affordability_score: "Affordability",
  boc_policy_rate: "Bank of Canada policy rate",
  cad_usd_exchange_rate: "CAD/USD exchange rate"
};
