import { formatMetric, signedPercent } from "@/lib/formatters";
import type { LeaderboardRow } from "@/lib/types";
import { RankChangeBadge } from "./RankChangeBadge";

export function LeaderboardTable({ rows }: { rows: LeaderboardRow[] }) {
  return (
    <table className="compact-table">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Region</th>
          <th>Value</th>
          <th>YoY</th>
          <th>Rank change</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.location_id}>
            <td>{row.rank}</td>
            <td>{row.name}</td>
            <td>{formatMetric(row.value, row.unit)}</td>
            <td>{signedPercent(row.yoy_change)}</td>
            <td>
              <RankChangeBadge change={row.rank_change} />
            </td>
            <td>{row.updated}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
