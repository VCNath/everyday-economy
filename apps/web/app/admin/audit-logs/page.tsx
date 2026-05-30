"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminAuditLogs } from "@/lib/api-client";
import type { AdminAuditLog } from "@/lib/types";

export default function AuditLogsPage() {
  const auth = useAuth();
  const [logs, setLogs] = useState<AdminAuditLog[]>([]);
  useEffect(() => {
    if (!auth.token) return;
    getAdminAuditLogs(auth.token, { limit: 200 }).then(setLogs);
  }, [auth.token]);

  return (
    <AppShell>
      <PageHeader title="Audit Logs" subtitle="Admin mutation audit history." />
      <AdminGuard>
        <section className="panel">
          <table className="compact-table">
            <thead><tr><th>Action</th><th>User</th><th>Entity</th><th>Details</th><th>Created</th></tr></thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td>{log.action}</td>
                  <td>{log.user_id ?? "-"}</td>
                  <td>{log.entity_type ?? "-"} {log.entity_id ?? ""}</td>
                  <td>{log.details ? JSON.stringify(log.details) : "-"}</td>
                  <td>{log.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}

