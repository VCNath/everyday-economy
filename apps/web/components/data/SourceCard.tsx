import type { SourceStatus } from "@/lib/types";

export function SourceCard({ source }: { source: SourceStatus }) {
  return (
    <article className="panel source-card">
      <span className="badge positive">{source.status}</span>
      <h2>{source.source}</h2>
      <p>{source.dataset}</p>
      <dl>
        <div><dt>Latest period</dt><dd>{source.latest_period}</dd></div>
        <div><dt>Last checked</dt><dd>{source.last_checked}</dd></div>
      </dl>
    </article>
  );
}
