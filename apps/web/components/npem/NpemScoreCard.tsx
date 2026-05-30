import { GlassCard } from "@/components/ui/GlassCard";
import { StatusPill } from "@/components/ui/StatusPill";
import type { NpemScore } from "@/lib/types";

export function NpemScoreCard({ score }: { score: NpemScore }) {
  return (
    <GlassCard className="metric-card">
      <div className="row between">
        <span className="eyebrow">{score.group_layer === "overlay" ? "Overlay cohort" : "Core archetype"}</span>
        <StatusPill label={`Confidence ${score.confidence.confidence_grade}`} tone={score.confidence.confidence_grade === "A" || score.confidence.confidence_grade === "B" ? "positive" : "warning"} />
      </div>
      <h3>{score.group_label}</h3>
      <div className="metric-value">{score.final_score?.toFixed(1) ?? "-"}</div>
      <p>Rank #{score.rank ?? "-"} in {score.geography_code}. PAF {score.paf_value?.toFixed(3) ?? "1.000"}.</p>
    </GlassCard>
  );
}
