import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { InsightFeed } from "@/components/insights/InsightFeed";
import { InsightFilters } from "@/components/insights/InsightFilters";
import { getRegionSummary, getSourceStatus } from "@/lib/api-client";
import { buildInsights } from "@/lib/insights";

export default async function InsightsPage() {
  const [national, selectedRegion, sourceStatus] = await Promise.all([
    getRegionSummary("CA"),
    getRegionSummary("CA-SK"),
    getSourceStatus()
  ]);
  const insights = buildInsights({ national, selectedRegion, sourceStatus });
  return (
    <AppShell>
      <PageHeader title="Insights" subtitle="Plain-English economic briefings generated from dashboard data." />
      <InsightFilters />
      <InsightFeed insights={insights} />
    </AppShell>
  );
}
