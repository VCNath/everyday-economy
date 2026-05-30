export type GeographyLevel = "country" | "province" | "territory" | "cma" | "city";

export type MetricKey =
  | "cpi_all_items_index"
  | "cpi_all_items_yoy"
  | "cpi_food_index"
  | "cpi_food_yoy"
  | "cpi_shelter_index"
  | "cpi_shelter_yoy"
  | "gas_regular_cents_litre"
  | "unemployment_rate"
  | "employment_rate"
  | "participation_rate"
  | "basic_basket_monthly_cost"
  | "basic_basket_yoy"
  | "affordability_score"
  | "boc_policy_rate"
  | "cad_usd_exchange_rate";

export interface Location {
  id: string;
  name: string;
  country_code: string;
  region_code?: string;
  geography_level: GeographyLevel;
  latitude: number;
  longitude: number;
}

export interface LeaderboardRow {
  rank: number;
  location_id: string;
  name: string;
  value: number;
  unit: string;
  yoy_change?: number;
  mom_change?: number;
  previous_rank?: number;
  rank_change?: number;
  source: string;
  updated: string;
}
