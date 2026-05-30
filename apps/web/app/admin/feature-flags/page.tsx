"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminFeatureFlags, updateAdminFeatureFlag } from "@/lib/api-client";
import type { FeatureFlag } from "@/lib/types";

export default function FeatureFlagsPage() {
  const auth = useAuth();
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  useEffect(() => {
    if (!auth.token) return;
    getAdminFeatureFlags(auth.token).then(setFlags);
  }, [auth.token]);

  return (
    <AppShell>
      <PageHeader title="Feature Flags" subtitle="Runtime switches for unfinished features." />
      <AdminGuard>
        <section className="panel page-panel">
          <table className="compact-table">
            <thead><tr><th>Flag</th><th>Status</th><th>Description</th><th>Updated</th></tr></thead>
            <tbody>
              {flags.map((flag) => (
                <tr key={flag.key}>
                  <td>{flag.key}</td>
                  <td>
                    <button
                      className="button"
                      type="button"
                      onClick={async () => {
                        if (!auth.token) return;
                        const updated = await updateAdminFeatureFlag(auth.token, flag.key, {
                          enabled: !flag.enabled,
                          description: flag.description ?? undefined,
                        });
                        setFlags((current) => current.map((row) => (row.key === flag.key ? updated : row)));
                      }}
                    >
                      {flag.enabled ? "Enabled" : "Disabled"}
                    </button>
                  </td>
                  <td>{flag.description ?? "-"}</td>
                  <td>{flag.updated_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}
