import type { LeaderboardRow, MapFeature, RegionSummary, SourceStatus } from "./types";

export const mapFeatures: MapFeature[] = [
  { location_id: "CA-BC", name: "British Columbia", value: 5.8, rank: 11, geometry_ref: "CA-BC", updated: "2026-04" },
  { location_id: "CA-AB", name: "Alberta", value: 4.2, rank: 8, geometry_ref: "CA-AB", updated: "2026-04" },
  { location_id: "CA-SK", name: "Saskatchewan", value: 3.7, rank: 6, geometry_ref: "CA-SK", updated: "2026-04" },
  { location_id: "CA-MB", name: "Manitoba", value: 3.5, rank: 4, geometry_ref: "CA-MB", updated: "2026-04" },
  { location_id: "CA-ON", name: "Ontario", value: 4.9, rank: 9, geometry_ref: "CA-ON", updated: "2026-04" },
  { location_id: "CA-QC", name: "Quebec", value: 3.2, rank: 3, geometry_ref: "CA-QC", updated: "2026-04" },
  { location_id: "CA-NB", name: "New Brunswick", value: 3.6, rank: 5, geometry_ref: "CA-NB", updated: "2026-04" },
  { location_id: "CA-NS", name: "Nova Scotia", value: 4.1, rank: 7, geometry_ref: "CA-NS", updated: "2026-04" },
  { location_id: "CA-PE", name: "Prince Edward Island", value: 3.8, rank: 6, geometry_ref: "CA-PE", updated: "2026-04" },
  { location_id: "CA-NL", name: "Newfoundland and Labrador", value: 4.4, rank: 8, geometry_ref: "CA-NL", updated: "2026-04" },
  { location_id: "CA-YT", name: "Yukon", value: 5.1, rank: 10, geometry_ref: "CA-YT", updated: "2026-04" },
  { location_id: "CA-NT", name: "Northwest Territories", value: 6.2, rank: 12, geometry_ref: "CA-NT", updated: "2026-04" },
  { location_id: "CA-NU", name: "Nunavut", value: 7.4, rank: 13, geometry_ref: "CA-NU", updated: "2026-04" }
];

export const saskatchewanSummary: RegionSummary = {
  location_id: "CA-SK",
  name: "Saskatchewan",
  period: "2026-04",
  metrics: {
    cpi_all_items_yoy: 2.4,
    cpi_food_yoy: 3.7,
    gas_regular_cents_litre: 154.2,
    unemployment_rate: 5.6,
    basic_basket_monthly_cost: 428.35,
    affordability_score: 72
  },
  insight: "Prices are rising slower than the national average, but food and fuel remain the biggest pressure points.",
  sources: ["Statistics Canada", "Internal composite"]
};

export const groceryLeaderboard: LeaderboardRow[] = [
  { rank: 1, location_id: "CA-NU", name: "Nunavut", value: 612.4, unit: "CAD/month", yoy_change: 7.4, previous_rank: 1, rank_change: 0, source: "Statistics Canada", updated: "2026-04" },
  { rank: 2, location_id: "CA-NT", name: "Northwest Territories", value: 528.9, unit: "CAD/month", yoy_change: 6.2, previous_rank: 2, rank_change: 0, source: "Statistics Canada", updated: "2026-04" },
  { rank: 3, location_id: "CA-YT", name: "Yukon", value: 501.2, unit: "CAD/month", yoy_change: 5.1, previous_rank: 4, rank_change: 1, source: "Statistics Canada", updated: "2026-04" },
  { rank: 4, location_id: "CA-BC", name: "British Columbia", value: 487.22, unit: "CAD/month", yoy_change: 5.8, previous_rank: 3, rank_change: -1, source: "Statistics Canada", updated: "2026-04" },
  { rank: 5, location_id: "CA-ON", name: "Ontario", value: 462.18, unit: "CAD/month", yoy_change: 4.9, previous_rank: 5, rank_change: 0, source: "Statistics Canada", updated: "2026-04" }
];

export const sourceStatus: SourceStatus[] = [
  { source: "Statistics Canada", dataset: "CPI", latest_period: "2026-04", last_checked: "2026-05-27", status: "Healthy" },
  { source: "Statistics Canada", dataset: "Food Prices", latest_period: "2026-03", last_checked: "2026-05-27", status: "Healthy" },
  { source: "Statistics Canada", dataset: "Gasoline", latest_period: "2026-04", last_checked: "2026-05-27", status: "Healthy" },
  { source: "Bank of Canada", dataset: "Rates and FX", latest_period: "2026-05-27", last_checked: "2026-05-27", status: "Healthy" }
];
