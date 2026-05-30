import type { NpemScenarioDelta } from "@/lib/types";

export function NpemScenarioDeltaTable({ rows }: { rows: NpemScenarioDelta[] }) {
  return (
    <section className="panel">
      <h3>Scenario Deltas</h3>
      <table className="compact-table">
        <thead><tr><th>Group</th><th>Baseline</th><th>Scenario</th><th>Delta</th><th>Rank change</th></tr></thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.group_code}>
              <td>{row.group_label}</td>
              <td>{row.scenario_a_score?.toFixed(1) ?? "-"}</td>
              <td>{row.scenario_b_score?.toFixed(1) ?? "-"}</td>
              <td>{row.delta?.toFixed(1) ?? "-"}</td>
              <td>{row.rank_change ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
