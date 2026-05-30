import type { LeaderboardRow } from "@/lib/types";
import { LeaderboardTable } from "./LeaderboardTable";
import { LeaderboardTabs } from "./LeaderboardTabs";

export function LeaderboardPanel({ rows }: { rows: LeaderboardRow[] }) {
  return (
    <section className="panel leaderboard-panel">
      <div className="panel-header">
        <div>
          <p className="muted">Leaderboards</p>
          <h2 className="section-title">Most expensive grocery basket</h2>
        </div>
      </div>
      <LeaderboardTabs />
      <LeaderboardTable rows={rows} />
    </section>
  );
}
