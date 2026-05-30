import { StatusPill } from "@/components/ui/StatusPill";
import type { NpemScore } from "@/lib/types";

export function NpemConfidencePanel({ score }: { score?: NpemScore }) {
  if (!score) return null;
  return (
    <section className="panel">
      <div className="row between">
        <h3>Confidence</h3>
        <StatusPill label={`${score.confidence.confidence_grade} · ${score.confidence.confidence_label}`} tone="info" />
      </div>
      <div className="metric-row"><span>Coverage</span><strong>{Math.round((score.confidence.coverage_ratio ?? 0) * 100)}%</strong></div>
      <div className="metric-row"><span>Directness</span><strong>{Math.round((score.confidence.directness_score ?? 0) * 100)}%</strong></div>
      <div className="metric-row"><span>Proxy share</span><strong>{Math.round((score.confidence.proxy_share ?? 0) * 100)}%</strong></div>
      <p>Scores marked D or E should be treated as low-confidence or experimental, especially for small-cell overlays.</p>
    </section>
  );
}
