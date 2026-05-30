import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemComponentBreakdown } from "@/components/npem/NpemComponentBreakdown";
import { NpemConfidencePanel } from "@/components/npem/NpemConfidencePanel";
import { NpemHeatmap } from "@/components/npem/NpemHeatmap";
import { NpemMethodologyNote } from "@/components/npem/NpemMethodologyNote";
import { NpemProvenancePanel } from "@/components/npem/NpemProvenancePanel";
import { NpemScenarioDeltaTable } from "@/components/npem/NpemScenarioDeltaTable";
import { NpemScenarioSelector } from "@/components/npem/NpemScenarioSelector";
import { NpemScoreCard } from "@/components/npem/NpemScoreCard";
import { compareNpemScenarios, getNpemProvenance, getNpemScenarios, getNpemScores } from "@/lib/api-client";

export default async function NpemPage({ searchParams }: { searchParams?: Promise<{ province?: string; scenario?: string }> }) {
  const params = (await searchParams) ?? {};
  const province = params.province ?? "AB";
  const scenario = params.scenario ?? "baseline";
  const [scores, scenarios, deltas, provenance] = await Promise.all([
    getNpemScores({ province, scenario }),
    getNpemScenarios(),
    compareNpemScenarios({ province, scenario_a: "baseline", scenario_b: "housing_stress" }),
    getNpemProvenance({ province, group: "YA_UC" })
  ]);
  const top = scores.scores[0];
  const pressured = scores.scores[scores.scores.length - 1];
  const averageConfidence = Math.round(scores.scores.reduce((sum, row) => sum + row.confidence.confidence_score, 0) / Math.max(1, scores.scores.length));

  return (
    <AppShell>
      <PageHero
        eyebrow="N.P.E.M."
        title="National Personal Economic Model"
        body="Compare economic pressure and resilience across Canadian demographic archetypes with scenario weights, confidence grades, and citation-ready provenance."
      />
      <section className="freshness-strip">
        <span>Province: {scores.geography_code}</span>
        <span>Year: {scores.reference_year}</span>
        <span>Model: {scores.model_version}</span>
        <span>Demo/estimated scaffold</span>
      </section>
      <NpemScenarioSelector scenarios={scenarios} active={scenario} />
      <section className="content-grid three">
        {top ? <NpemScoreCard score={top} /> : null}
        {pressured ? <NpemScoreCard score={pressured} /> : null}
        <div className="panel metric-card">
          <span className="eyebrow">Average confidence</span>
          <div className="metric-value">{averageConfidence}</div>
          <p>Confidence combines coverage, recency, directness, reliability, proxy share, and suppression risk.</p>
        </div>
      </section>
      <NpemHeatmap scores={scores.scores} />
      <div className="two-col">
        <NpemScenarioDeltaTable rows={deltas} />
        <NpemComponentBreakdown score={top} />
      </div>
      <div className="two-col">
        <NpemConfidencePanel score={top} />
        <NpemProvenancePanel rows={provenance} />
      </div>
      <NpemMethodologyNote />
    </AppShell>
  );
}
