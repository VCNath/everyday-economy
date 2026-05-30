"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminDataQualityFlags, markDataQualityFlagReviewed } from "@/lib/api-client";
import type { DataQualityFlag } from "@/lib/types";

export default function DataQualityPage() {
  const auth = useAuth();
  const [flags, setFlags] = useState<DataQualityFlag[]>([]);

  async function refresh() {
    if (!auth.token) return;
    setFlags(await getAdminDataQualityFlags(auth.token));
  }

  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <AppShell>
      <PageHeader title="Data Quality" subtitle="Operational data quality flags and review state." />
      <AdminGuard>
        <section className="panel">
          <table className="compact-table">
            <thead><tr><th>Severity</th><th>Flag</th><th>Message</th><th>Created</th><th>Reviewed</th><th>Action</th></tr></thead>
            <tbody>
              {flags.map((flag) => (
                <tr key={flag.id}>
                  <td>{flag.severity}</td>
                  <td>{flag.flag_type}</td>
                  <td>{flag.message ?? "-"}</td>
                  <td>{flag.created_at}</td>
                  <td>{flag.reviewed_at ?? "No"}</td>
                  <td>
                    {!flag.reviewed_at ? (
                      <button
                        className="button"
                        type="button"
                        onClick={async () => {
                          if (!auth.token) return;
                          await markDataQualityFlagReviewed(auth.token, flag.id, "Reviewed in admin UI");
                          await refresh();
                        }}
                      >
                        Mark reviewed
                      </button>
                    ) : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}

