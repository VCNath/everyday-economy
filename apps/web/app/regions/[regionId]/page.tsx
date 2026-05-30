import { AppShell } from "@/components/layout/AppShell";
import { RegionBasketBreakdown } from "@/components/regions/RegionBasketBreakdown";
import { RegionHeader } from "@/components/regions/RegionHeader";
import { RegionInsightSummary } from "@/components/regions/RegionInsightSummary";
import { RegionKpiGrid } from "@/components/regions/RegionKpiGrid";
import { RegionLeaderboardRanks } from "@/components/regions/RegionLeaderboardRanks";
import { RegionSourceNotes } from "@/components/regions/RegionSourceNotes";
import { RegionTrendCharts } from "@/components/regions/RegionTrendCharts";
import { getRegionSummary, getRegionTimeSeries } from "@/lib/api-client";

export default async function RegionProfilePage({
  params,
  searchParams
}: {
  params: Promise<{ regionId: string }>;
  searchParams?: Promise<{ indicators?: string; window?: string }>;
}) {
  const { regionId } = await params;
  const filters = (await searchParams) ?? {};
  const indicators = filters.indicators ? filters.indicators.split(",").filter(Boolean) : [
    "cpi_all_items_yoy",
    "cpi_food_yoy",
    "gas_regular_cents_litre",
    "unemployment_rate"
  ];
  const [summary, series] = await Promise.all([
    getRegionSummary(regionId),
    getRegionTimeSeries(regionId, {
      indicators,
      window: filters.window ?? "12m",
      include_freshness: true
    })
  ]);
  const firstSeries = series.series[0];
  const points = (firstSeries?.points ?? []).map((point) => point.value ?? 0);
  return (
    <AppShell>
      <RegionHeader name={summary.name} locationId={regionId} />
      <section className="freshness-strip">
        <span>Window: {series.window}</span>
        <span>End period: {series.end_period ?? "latest"}</span>
        <span>Warnings: {series.warnings.length}</span>
      </section>
      <RegionKpiGrid summary={summary} />
      <div className="two-col"><RegionTrendCharts points={points} /><RegionInsightSummary /></div>
      <RegionLeaderboardRanks />
      <RegionBasketBreakdown />
      <RegionSourceNotes />
    </AppShell>
  );
}
