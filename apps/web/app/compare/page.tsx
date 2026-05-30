import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { CompareExportButton } from "@/components/compare/CompareExportButton";
import { CompareInsightSummary } from "@/components/compare/CompareInsightSummary";
import { CompareKpiGrid } from "@/components/compare/CompareKpiGrid";
import { CompareMetricTable } from "@/components/compare/CompareMetricTable";
import { CompareRegionSelector } from "@/components/compare/CompareRegionSelector";
import { CompareTrendChart } from "@/components/compare/CompareTrendChart";
import { getCompareRegions } from "@/lib/api-client";

const DEFAULT_REGIONS = ["CA-SK", "CA-AB", "CA-MB"];

export default async function ComparePage({
  searchParams
}: {
  searchParams?: Promise<{ regions?: string; window?: string; indicators?: string }>;
}) {
  const params = (await searchParams) ?? {};
  const regionIds = params.regions ? params.regions.split(",").filter(Boolean) : DEFAULT_REGIONS;
  const indicators = params.indicators ? params.indicators.split(",").filter(Boolean) : [
    "cpi_all_items_yoy",
    "cpi_food_yoy",
    "cpi_shelter_yoy",
    "gas_regular_cents_litre",
    "unemployment_rate",
    "basic_basket_monthly_cost",
    "affordability_score"
  ];
  const compare = await getCompareRegions(regionIds, indicators, { window: params.window ?? "12m" });
  const affordabilityRows = compare.rows.filter((row) => row.indicator_id === "affordability_score");
  const locationNames = compare.locations.map((location) => location.location_name);
  return (
    <AppShell>
      <PageHeader title="Compare Regions" subtitle="Compare inflation, groceries, gas, jobs, housing, and affordability." primaryAction={<CompareExportButton />} />
      <section className="freshness-strip">
        <span>Window: {compare.window}</span>
        <span>Period: {compare.period}</span>
        <span>Warnings: {compare.warnings.length}</span>
      </section>
      <section className="panel page-panel"><CompareRegionSelector /></section>
      <CompareKpiGrid rows={affordabilityRows} metricLabel="Affordability" />
      <div className="two-col"><CompareTrendChart /><CompareInsightSummary insight="Comparison uses latest available source observations with fallback flags when needed." /></div>
      <CompareMetricTable rows={compare.rows} locationNames={locationNames} />
    </AppShell>
  );
}
