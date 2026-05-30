"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { generateMonthlyReport, getMonthlyReports, getSavedRegions } from "@/lib/api-client";
import type { MonthlyReport, SavedRegion } from "@/lib/types";

export default function ReportsPage() {
  const auth = useAuth();
  const [reports, setReports] = useState<MonthlyReport[]>([]);
  const [saved, setSaved] = useState<SavedRegion[]>([]);

  async function refresh() {
    if (!auth.token) return;
    const [reportRows, savedRows] = await Promise.all([getMonthlyReports(auth.token), getSavedRegions(auth.token)]);
    setReports(reportRows);
    setSaved(savedRows);
  }
  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!auth.isAuthenticated) {
    return (
      <AppShell>
        <PageHeader title="Monthly Reports" subtitle="Generated summaries for your saved regions." />
        <EmptyState title="Sign in to generate reports" body="Reports help you track monthly affordability changes in your watchlist." action="Log in" href="/auth/login" />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Monthly Reports" subtitle="Deterministic monthly affordability summaries." />
      <section className="panel">
        <strong>Generate</strong>
        <div className="row">
          {saved.map((region) => (
            <button key={region.location_id} className="button" type="button" onClick={async () => { if (!auth.token) return; await generateMonthlyReport(auth.token, region.location_id); await refresh(); }}>
              {region.name}
            </button>
          ))}
        </div>
      </section>
      {reports.length === 0 ? (
        <EmptyState title="No reports yet" body="Generate a report from your saved regions to start monthly tracking." />
      ) : (
        <section className="stack">
          {reports.map((report) => (
            <article className="panel" key={report.id}>
              <strong>{report.title}</strong>
              <p>{report.summary}</p>
              <small>{report.report_period} · Generated {report.generated_at}</small>
            </article>
          ))}
        </section>
      )}
    </AppShell>
  );
}

