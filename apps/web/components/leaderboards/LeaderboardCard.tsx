import { LeaderboardTable } from "@/components/leaderboard/LeaderboardTable";
import { FreshnessBadge } from "@/components/data/FreshnessBadge";
import type { LeaderboardRow } from "@/lib/types";

export function LeaderboardCard({ rows }: { rows: LeaderboardRow[] }) {
  return (
    <section className="panel leaderboard-card">
      <p className="muted">Latest period: Apr 2026</p>
      <FreshnessBadge status="healthy" />
      <h2 className="section-title">Most expensive grocery basket</h2>
      <LeaderboardTable rows={rows} />
    </section>
  );
}
