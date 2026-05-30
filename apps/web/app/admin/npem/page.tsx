"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatusPill } from "@/components/ui/StatusPill";
import { useAuth } from "@/hooks/useAuth";
import { getNpemScenarios, getNpemScores, triggerAdminJob } from "@/lib/api-client";
import type { NpemScenario, NpemScoreResponse } from "@/lib/types";

export default function AdminNpemPage() {
  const auth = useAuth();
  const [scores, setScores] = useState<NpemScoreResponse | null>(null);
  const [scenarios, setScenarios] = useState<NpemScenario[]>([]);

  async function refresh() {
    const [scoreData, scenarioData] = await Promise.all([getNpemScores({ province: "AB" }), getNpemScenarios()]);
    setScores(scoreData);
    setScenarios(scenarioData);
  }

  useEffect(() => { void refresh(); }, []);

  async function calculate() {
    if (!auth.token) return;
    if (!window.confirm("Calculate deterministic N.P.E.M. demo scores now?")) return;
    await triggerAdminJob(auth.token, "calculate-npem");
    await refresh();
  }

  const lowConfidence = scores?.scores.filter((row) => ["D", "E"].includes(row.confidence.confidence_grade)).length ?? 0;

  return (
    <AppShell>
      <PageHeader title="N.P.E.M. Operations" subtitle="Model version, scenarios, confidence, validation, and scoring controls." />
      <AdminGuard>
        <section className="content-grid three">
          <div className="panel metric-card"><span className="eyebrow">Model version</span><strong>{scores?.model_version ?? "npem_v1_demo_2026"}</strong></div>
          <div className="panel metric-card"><span className="eyebrow">Scenarios</span><strong>{scenarios.length}</strong></div>
          <div className="panel metric-card"><span className="eyebrow">Low confidence</span><strong>{lowConfidence}</strong></div>
        </section>
        <section className="panel">
          <div className="row between">
            <h3>Scenario Weights</h3>
            <button className="button" type="button" onClick={calculate}>Calculate N.P.E.M.</button>
          </div>
          <table className="compact-table">
            <thead><tr><th>Scenario</th><th>Model</th><th>Status</th><th>Weights Sum</th></tr></thead>
            <tbody>
              {scenarios.map((scenario) => (
                <tr key={scenario.scenario_code}>
                  <td>{scenario.label}</td>
                  <td>{scenario.model_version}</td>
                  <td><StatusPill label={scenario.enabled ? "Enabled" : "Disabled"} tone={scenario.enabled ? "positive" : "neutral"} /></td>
                  <td>{Object.values(scenario.weights).reduce((sum, weight) => sum + weight, 0).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
        <section className="panel">
          <h3>Operational Notes</h3>
          <p>Current N.P.E.M. outputs are deterministic demo estimates with provenance records. Production source adapters should replace seeded raw values before public ranking claims.</p>
        </section>
      </AdminGuard>
    </AppShell>
  );
}
