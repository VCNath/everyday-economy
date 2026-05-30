import type { LeaderboardRow } from "@/lib/types";
import { signedPercent } from "@/lib/formatters";

export function BiggestMovers({ rows }: { rows: LeaderboardRow[] }) {
  return (
    <section className="panel movers-panel">
      <p className="muted">Biggest monthly movers</p>
      <h2 className="section-title">Regions changing fastest</h2>
      <div className="mover-list">
        {rows.slice(0, 5).map((row, index) => (
          <article key={row.location_id}>
            <span>{index + 1}</span>
            <div>
              <strong>{row.name}</strong>
              <small>{signedPercent(row.mom_change)} month over month</small>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
