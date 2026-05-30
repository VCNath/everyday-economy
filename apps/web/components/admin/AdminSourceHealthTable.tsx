import type { AdminJobRun, AdminSourceHealth, SourceRun, SourceStatus } from "@/lib/types";

export function AdminSourceHealthTable({
  sources = [],
  runs = [],
}: {
  sources?: Array<SourceStatus | AdminSourceHealth>;
  runs?: Array<SourceRun | AdminJobRun>;
}) {
  return (
    <section className="panel">
      <table className="compact-table">
        <thead><tr><th>Source</th><th>Dataset</th><th>Status</th><th>Last Run</th><th>Rows</th><th>Error</th></tr></thead>
        <tbody>
          {sources.map((source) => {
            const sourceName = source.source;
            const dataset = source.dataset;
            const lastChecked = source.last_checked;
            const run = runs.find((candidate) => {
              const sourceId = "source_id" in candidate ? (candidate.source_id ?? "") : "";
              return sourceName.toLowerCase().includes(sourceId.replaceAll("_", " "));
            });
            return (
              <tr key={`${sourceName}-${dataset}`}>
                <td>{sourceName}</td>
                <td>{dataset}</td>
                <td>{source.status}</td>
                <td>{("finished_at" in (run ?? {}) ? run?.finished_at : undefined) ?? lastChecked}</td>
                <td>{run ? `${run.rows_fetched}/${run.rows_inserted}/${run.rows_updated}` : "rows_fetched" in source ? `${source.rows_fetched}/${source.rows_inserted}/${source.rows_updated}` : "-"}</td>
                <td>{(run?.error_message as string | undefined) ?? ("error_message" in source ? source.error_message : undefined) ?? "-"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}
