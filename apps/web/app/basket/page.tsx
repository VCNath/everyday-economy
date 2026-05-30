import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageToolbar } from "@/components/layout/PageToolbar";
import { BasketRegionSelector } from "@/components/basket/BasketRegionSelector";
import { BasketTypeSelector } from "@/components/basket/BasketTypeSelector";
import { HouseholdSizeSelector } from "@/components/basket/HouseholdSizeSelector";
import { BasketSummaryCard } from "@/components/basket/BasketSummaryCard";
import { BasketDriversPanel } from "@/components/basket/BasketDriversPanel";
import { BasketItemTable } from "@/components/basket/BasketItemTable";
import { BasketLeaderboard } from "@/components/basket/BasketLeaderboard";
import { BasketMethodology } from "@/components/basket/BasketMethodology";
import { getBasketDefault, getLeaderboardsByParams } from "@/lib/api-client";

export default async function BasketPage() {
  const [basket, leaderboard] = await Promise.all([
    getBasketDefault(),
    getLeaderboardsByParams({ type: "most_expensive_groceries", limit: 10 })
  ]);
  const rows = leaderboard.rows;
  return (
    <AppShell>
      <PageHeader title="Basket Builder" subtitle="Build a basic monthly basket and compare regions." />
      <section className="freshness-strip">
        <span>Latest basket period: {basket.period}</span>
        <span>Coverage score: {(basket.coverage_score * 100).toFixed(0)}%</span>
      </section>
      <PageToolbar><HouseholdSizeSelector /><BasketTypeSelector /><BasketRegionSelector /></PageToolbar>
      <div className="two-col"><BasketSummaryCard /><BasketDriversPanel /></div>
      <BasketItemTable />
      <BasketLeaderboard rows={rows} />
      <BasketMethodology />
    </AppShell>
  );
}
