import { EconomicMap } from "@/components/map/EconomicMap";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageToolbar } from "@/components/layout/PageToolbar";
import { RightDrawer } from "@/components/layout/RightDrawer";
import { AppShell } from "@/components/layout/AppShell";
import { Select } from "@/components/ui/Select";
import { getMapData, getRegionSummary } from "@/lib/api-client";
import { RegionSummaryCard } from "@/components/cards/RegionSummaryCard";

export default async function MapPage() {
  const [mapData, summary] = await Promise.all([getMapData(), getRegionSummary("CA-SK")]);
  return (
    <AppShell>
      <PageHeader title="Map Explorer" subtitle="Explore economic pressure by region, metric, and period." />
      <section className="freshness-strip">
        <span>Source: {mapData.source}</span>
        <span>Latest period: {mapData.period}</span>
      </section>
      <PageToolbar>
        <Select label="Metric" options={["CPI", "Food CPI", "Grocery Basket", "Gas", "Jobs", "Housing", "Affordability"]} />
        <Select label="Geography" options={["Province", "CMA", "City"]} />
        <Select label="Display" options={["Value", "YoY", "MoM", "Rank"]} />
        <Select label="Period" options={["Latest", "1M", "3M", "12M", "Custom"]} />
      </PageToolbar>
      <div className="map-explorer-grid">
        <EconomicMap features={mapData.features} />
        <RightDrawer title="Region detail"><RegionSummaryCard summary={summary} /></RightDrawer>
      </div>
    </AppShell>
  );
}
