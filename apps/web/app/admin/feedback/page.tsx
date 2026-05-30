"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatusPill } from "@/components/ui/StatusPill";
import { useAuth } from "@/hooks/useAuth";
import { getAdminFeedback, updateAdminFeedbackStatus } from "@/lib/api-client";
import type { BetaFeedback, FeedbackStatus } from "@/lib/types";

const STATUSES: FeedbackStatus[] = ["new", "reviewed", "planned", "fixed", "closed"];

export default function AdminFeedbackPage() {
  const auth = useAuth();
  const [rows, setRows] = useState<BetaFeedback[]>([]);
  const [statusFilter, setStatusFilter] = useState("");

  async function refresh() {
    if (!auth.token) return;
    setRows(await getAdminFeedback(auth.token, { status: statusFilter || undefined, limit: 100 }));
  }

  useEffect(() => { void refresh(); }, [auth.token, statusFilter]); // eslint-disable-line react-hooks/exhaustive-deps

  async function updateStatus(id: string, status: FeedbackStatus) {
    if (!auth.token) return;
    await updateAdminFeedbackStatus(auth.token, id, status);
    await refresh();
  }

  return (
    <AppShell>
      <PageHeader title="Beta Feedback" subtitle="Review public beta feedback, data issues, and product confusion reports." />
      <AdminGuard>
        <section className="panel page-panel">
          <div className="row between wrap">
            <label className="field compact-field">
              <span>Status</span>
              <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
                <option value="">All</option>
                {STATUSES.map((status) => <option key={status} value={status}>{status}</option>)}
              </select>
            </label>
            <StatusPill label={`${rows.length} reports`} tone="info" />
          </div>
        </section>
        <section className="panel">
          <table className="compact-table">
            <thead>
              <tr><th>Type</th><th>Status</th><th>Page</th><th>Message</th><th>Rating</th><th>Created</th><th>Update</th></tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id}>
                  <td>{row.feedback_type}</td>
                  <td><StatusPill label={row.status} tone={row.status === "new" ? "warning" : row.status === "fixed" || row.status === "closed" ? "positive" : "info"} /></td>
                  <td>{row.page_path ?? "-"}</td>
                  <td>{row.message.slice(0, 140)}{row.message.length > 140 ? "..." : ""}</td>
                  <td>{row.rating ?? "-"}</td>
                  <td>{row.created_at}</td>
                  <td>
                    <select aria-label={`Update feedback ${row.id}`} value={row.status} onChange={(event) => updateStatus(row.id, event.target.value as FeedbackStatus)}>
                      {STATUSES.map((status) => <option key={status} value={status}>{status}</option>)}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!rows.length ? <p>No feedback matches this filter yet.</p> : null}
        </section>
      </AdminGuard>
    </AppShell>
  );
}
