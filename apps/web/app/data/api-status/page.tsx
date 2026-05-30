import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { SourceHealthTable } from "@/components/data/SourceHealthTable";
import { DataFreshnessTimeline } from "@/components/data/DataFreshnessTimeline";
import { getApiHealth, getSourceStatus } from "@/lib/api-client";

export default async function ApiStatusPage() {
  const [sources, health] = await Promise.all([getSourceStatus(), getApiHealth()]);
  const healthy = sources.filter((source) => source.status.toLowerCase() === "healthy").length;
  const stale = sources.filter((source) => source.status.toLowerCase() === "stale").length;
  const error = sources.filter((source) => source.status.toLowerCase() === "error").length;
  const partial = sources.filter((source) => source.status.toLowerCase() === "partial").length;
  return (
    <AppShell>
      <PageHeader title="API Status" subtitle="Data freshness and source health for public dashboard signals." />
      <section className="kpi-grid four">
        <article className="card"><p className="muted">Healthy sources</p><p className="metric-value">{healthy}</p></article>
        <article className="card"><p className="muted">Partial sources</p><p className="metric-value">{partial}</p></article>
        <article className="card"><p className="muted">Stale sources</p><p className="metric-value">{stale}</p></article>
        <article className="card"><p className="muted">Error sources</p><p className="metric-value">{error}</p></article>
      </section>
      <section className="freshness-strip">
        <span>API: {health.health.status}</span>
        <span>DB: {health.db.status}</span>
        <span>Cache: {health.cache.status}</span>
      </section>
      <section className="panel page-panel"><SourceHealthTable sources={sources} /></section>
      <DataFreshnessTimeline />
    </AppShell>
  );
}
