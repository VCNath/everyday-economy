import type { NpemScore } from "@/lib/types";

export function NpemComponentBreakdown({ score }: { score?: NpemScore }) {
  return (
    <section className="panel">
      <h3>Component Breakdown</h3>
      <div className="stack">
        {(score?.components ?? []).map((component) => (
          <div key={component.component_code} className="metric-row">
            <span>{component.component_code} · {component.component_label}</span>
            <strong>{component.normalized_score?.toFixed(1) ?? "-"}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
