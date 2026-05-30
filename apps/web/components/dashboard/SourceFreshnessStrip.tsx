import type { SourceStatus } from "@/lib/types";

export function SourceFreshnessStrip({ sources = [] }: { sources?: SourceStatus[] }) {
  const visible = sources.length
    ? sources.filter((source) => source.status !== "disabled").slice(0, 4)
    : [
        { source: "Statistics Canada", dataset: "CPI", latest_period: "2026-04", last_checked: "May 27, 2026", status: "healthy" },
        { source: "Statistics Canada", dataset: "Food prices", latest_period: "2026-03", last_checked: "May 27, 2026", status: "healthy" },
        { source: "Statistics Canada", dataset: "Gasoline", latest_period: "2026-04", last_checked: "May 27, 2026", status: "healthy" }
      ];
  return (
    <section className="freshness-strip">
      {visible.map((source) => (
        <span key={`${source.source}-${source.dataset}`}>{source.source} {source.dataset}: {source.latest_period}</span>
      ))}
    </section>
  );
}
