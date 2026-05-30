import type { NpemScore } from "@/lib/types";

export function NpemHeatmap({ scores }: { scores: NpemScore[] }) {
  return (
    <section className="panel">
      <h3>Province-by-Group Heatmap</h3>
      <div className="heatmap-grid">
        {scores.map((score) => (
          <div key={score.score_id} className="heatmap-cell">
            <span>{score.group_code}</span>
            <strong>{score.final_score?.toFixed(1) ?? "-"}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
