import type { SourceStatus } from "@/lib/types";

export function SourceHealthTable({ sources }: { sources: SourceStatus[] }) {
  return (
    <table className="compact-table">
      <thead><tr><th>Source</th><th>Dataset</th><th>Last check</th><th>Latest period</th><th>Status</th></tr></thead>
      <tbody>
        {sources.map((source) => (
          <tr key={`${source.source}-${source.dataset}`}>
            <td>{source.source}</td><td>{source.dataset}</td><td>{source.last_checked}</td><td>{source.latest_period}</td><td>{source.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
