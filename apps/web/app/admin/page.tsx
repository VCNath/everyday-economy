"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminJobRuns, getAdminSummary, triggerAdminJob } from "@/lib/api-client";
import type { AdminDashboardSummary, AdminJobRun } from "@/lib/types";

export default function AdminOverviewPage() {
  const auth = useAuth();
  const [summary, setSummary] = useState<AdminDashboardSummary | null>(null);
  const [runs, setRuns] = useState<AdminJobRun[]>([]);

  async function refresh() {
    if (!auth.token) return;
    const [s, r] = await Promise.all([getAdminSummary(auth.token), getAdminJobRuns(auth.token, { limit: 10 })]);
    setSummary(s);
    setRuns(r);
  }

  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  async function run(endpoint: string, confirmText: string) {
    if (!auth.token) return;
    if (!window.confirm(confirmText)) return;
    await triggerAdminJob(auth.token, endpoint);
    await refresh();
  }

  return (
    <AppShell>
      <PageHeader title="Admin Overview" subtitle="Operations status, recent runs, and quick actions." />
      <AdminGuard>
        <section className="panel page-panel">
          <div className="row wrap">
            <span>Healthy sources: {summary?.healthy_sources ?? 0}</span>
            <span>Stale sources: {summary?.stale_sources ?? 0}</span>
            <span>Failed jobs: {summary?.failed_jobs ?? 0}</span>
            <span>Open quality flags: {summary?.open_data_quality_flags ?? 0}</span>
          </div>
          <div className="row wrap">
            <button className="button" type="button" onClick={() => run("evaluate-alerts", "Run alert evaluation now?")}>Evaluate alerts</button>
            <button className="button" type="button" onClick={() => run("generate-monthly-reports", "Generate monthly reports now?")}>Generate monthly reports</button>
            <button className="button" type="button" onClick={() => run("build-leaderboards", "Build leaderboards now?")}>Build leaderboards</button>
            <button className="button" type="button" onClick={() => run("calculate-baskets", "Recalculate baskets now?")}>Calculate baskets</button>
          </div>
        </section>
        <section className="panel">
          <h3>Recent Job Runs</h3>
          <table className="compact-table">
            <thead><tr><th>Job</th><th>Status</th><th>Started</th><th>Duration</th><th>Rows Updated</th></tr></thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.id}>
                  <td>{run.job_name}</td>
                  <td>{run.status}</td>
                  <td>{run.started_at}</td>
                  <td>{run.duration_seconds ?? "-"}</td>
                  <td>{run.rows_updated}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}

