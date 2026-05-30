import { LeaderboardTable } from "@/components/leaderboard/LeaderboardTable";
import type { LeaderboardRow } from "@/lib/types";

export function BasketLeaderboard({ rows }: { rows: LeaderboardRow[] }) {
  return (
    <section className="panel">
      <h2 className="section-title">Regional basket leaderboard</h2>
      <LeaderboardTable rows={rows} />
    </section>
  );
}
