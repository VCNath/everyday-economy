import type { RegionSummary, SourceStatus } from "./types";

export type InsightSeverity = "info" | "positive" | "warning" | "negative";

export interface InsightItem {
  id: string;
  title: string;
  body: string;
  severity: InsightSeverity;
  metric?: string;
  region?: string;
  period: string;
  source: string;
}

export function buildInsights({
  national,
  selectedRegion,
  sourceStatus
}: {
  national: RegionSummary;
  selectedRegion: RegionSummary;
  sourceStatus: SourceStatus[];
}): InsightItem[] {
  const insights: InsightItem[] = [];
  const period = selectedRegion.period;
  if (selectedRegion.metrics.cpi_food_yoy > selectedRegion.metrics.cpi_all_items_yoy) {
    insights.push({
      id: "food-faster-than-cpi",
      title: "Food prices are rising faster than overall inflation",
      body: `${selectedRegion.name} food inflation is above its all-items CPI pace this period.`,
      severity: "warning",
      metric: "cpi_food_yoy",
      region: selectedRegion.name,
      period,
      source: "Statistics Canada"
    });
  }
  if (selectedRegion.metrics.cpi_all_items_yoy < national.metrics.cpi_all_items_yoy) {
    insights.push({
      id: "below-national-cpi",
      title: "Selected region is below national inflation",
      body: `${selectedRegion.name} CPI is currently below the Canada-wide inflation rate.`,
      severity: "positive",
      metric: "cpi_all_items_yoy",
      region: selectedRegion.name,
      period,
      source: "Statistics Canada"
    });
  }
  if (selectedRegion.metrics.unemployment_rate > national.metrics.unemployment_rate) {
    insights.push({
      id: "labour-softer-than-national",
      title: "Labour market is softer than national",
      body: `${selectedRegion.name} unemployment is above the national rate for this period.`,
      severity: "warning",
      metric: "unemployment_rate",
      region: selectedRegion.name,
      period,
      source: "Statistics Canada"
    });
  }
  const stale = sourceStatus.filter((source) => source.status.toLowerCase() === "stale");
  if (stale.length) {
    insights.push({
      id: "stale-source-warning",
      title: "Some source data is delayed",
      body: "Showing the latest available values for sources that have not updated recently.",
      severity: "negative",
      period,
      source: stale.map((item) => item.source).join(", ")
    });
  }
  if (!insights.length) {
    insights.push({
      id: "stable-conditions",
      title: "No major pressure spike detected",
      body: "Current indicators look relatively stable compared with recent fallback baselines.",
      severity: "info",
      period,
      source: "Statistics Canada"
    });
  }
  return insights;
}
