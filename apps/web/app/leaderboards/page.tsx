import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageTabs } from "@/components/layout/PageTabs";
import { LeaderboardFilters } from "@/components/leaderboards/LeaderboardFilters";
import { LeaderboardCard } from "@/components/leaderboards/LeaderboardCard";
import { RedFlagRegionsPanel } from "@/components/leaderboards/RedFlagRegionsPanel";
import { BiggestMoversPanel } from "@/components/leaderboards/BiggestMoversPanel";
import { LeaderboardMethodologyNote } from "@/components/leaderboards/LeaderboardMethodologyNote";
import { getLeaderboardsByParams } from "@/lib/api-client";

export default async function LeaderboardsPage() {
  const leaderboard = await getLeaderboardsByParams({ type: "most_expensive_groceries", limit: 10 });
  const rows = leaderboard.rows;
  return (
    <AppShell>
      <PageHeader title="Leaderboards" subtitle="See where costs are rising, falling, or biting hardest." primaryAction={<button className="button">Export CSV</button>} />
      <section className="freshness-strip">
        <span>Leaderboard: {leaderboard.leaderboard_type}</span>
        <span>Latest period: {leaderboard.period}</span>
      </section>
      <PageTabs tabs={["Overall", "Groceries", "Housing", "Gas", "Jobs", "Inflation", "Biggest Movers", "Most Improved", "Red Flags"]} active="Groceries" />
      <LeaderboardFilters />
      <LeaderboardCard rows={rows} />
      <div className="two-col"><BiggestMoversPanel rows={rows} /><RedFlagRegionsPanel /></div>
      <LeaderboardMethodologyNote />
    </AppShell>
  );
}
