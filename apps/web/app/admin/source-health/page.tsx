"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AdminSourceHealthTable } from "@/components/admin/AdminSourceHealthTable";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminSourceHealth, getAdminJobRuns } from "@/lib/api-client";
import type { AdminJobRun, AdminSourceHealth } from "@/lib/types";

export default function SourceHealthPage() {
  const auth = useAuth();
  const [sources, setSources] = useState<AdminSourceHealth[]>([]);
  const [runs, setRuns] = useState<AdminJobRun[]>([]);
  useEffect(() => {
    if (!auth.token) return;
    Promise.all([getAdminSourceHealth(auth.token), getAdminJobRuns(auth.token, { limit: 100 })]).then(([s, r]) => {
      setSources(s);
      setRuns(r);
    });
  }, [auth.token]);
  return (
    <AppShell>
      <PageHeader title="Source Health" subtitle="Admin source runs, rows, and errors." />
      <AdminGuard>
        <AdminSourceHealthTable sources={sources} runs={runs} />
      </AdminGuard>
    </AppShell>
  );
}
