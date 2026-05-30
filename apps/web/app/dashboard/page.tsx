import { AppShell } from "@/components/layout/AppShell";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { NationalKpiGrid } from "@/components/dashboard/NationalKpiGrid";
import { DashboardMapPreview } from "@/components/dashboard/DashboardMapPreview";
import { NationalSummaryPanel } from "@/components/dashboard/NationalSummaryPanel";
import { LeaderboardPreview } from "@/components/dashboard/LeaderboardPreview";
import { BiggestMoversPreview } from "@/components/dashboard/BiggestMoversPreview";
import { SavedRegionsPreview } from "@/components/dashboard/SavedRegionsPreview";
import { SourceFreshnessStrip } from "@/components/dashboard/SourceFreshnessStrip";
import { PersonalAlertsPanel } from "@/components/dashboard/PersonalAlertsPanel";
import { getLeaderboard, getMapFeatures, getSourceStatus } from "@/lib/api-client";

export default async function DashboardPage() {
  const [features, leaderboard, sources] = await Promise.all([getMapFeatures(), getLeaderboard("grocery_basket"), getSourceStatus()]);
  return (
    <AppShell>
      <DashboardHeader />
      <SourceFreshnessStrip sources={sources} />
      <NationalKpiGrid />
      <div className="grid-dashboard"><DashboardMapPreview features={features} /><NationalSummaryPanel /></div>
      <LeaderboardPreview rows={leaderboard} />
      <div className="two-col"><BiggestMoversPreview rows={leaderboard} /><SavedRegionsPreview /></div>
      <PersonalAlertsPanel />
    </AppShell>
  );
}
