"use client";

import { useEffect, useState } from "react";

import { AdminActionPanel } from "@/components/admin/AdminActionPanel";
import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminJobRuns, triggerAdminJob } from "@/lib/api-client";
import type { AdminJobRun } from "@/lib/types";

export default function DataIngestionPage() {
  const auth = useAuth();
  const [runs, setRuns] = useState<AdminJobRun[]>([]);

  async function refresh() {
    if (!auth.token) return;
    setRuns(await getAdminJobRuns(auth.token, { limit: 100 }));
  }

  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  async function runJob(endpoint: string) {
    if (!auth.token) return;
    if (!window.confirm(`Run ${endpoint} now?`)) return;
    await triggerAdminJob(auth.token, endpoint);
    await refresh();
  }

  return (
    <AppShell>
      <PageHeader title="Data Ingestion" subtitle="Admin-only source refresh actions. Hidden until roles are enabled." />
      <AdminGuard>
        <AdminActionPanel
          onRun={runJob}
          disabled={false}
        />
        <section className="panel">
          <table className="compact-table">
            <thead><tr><th>Job</th><th>Status</th><th>Started</th><th>Finished</th><th>Rows (f/i/u/f)</th><th>Error</th></tr></thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.id}>
                  <td>{run.job_name}</td>
                  <td>{run.status}</td>
                  <td>{run.started_at}</td>
                  <td>{run.finished_at ?? "-"}</td>
                  <td>{run.rows_fetched}/{run.rows_inserted}/{run.rows_updated}/{run.rows_failed}</td>
                  <td>{run.error_message ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}
