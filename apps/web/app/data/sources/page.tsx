import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { SourceCard } from "@/components/data/SourceCard";
import { getSourceStatus } from "@/lib/api-client";

export default async function SourcesPage() {
  const sources = await getSourceStatus();
  return (
    <AppShell>
      <PageHeader title="Sources" subtitle="Official data providers, datasets, freshness, and status." />
      <section className="source-grid">
        {sources.map((source) => <SourceCard key={`${source.source}-${source.dataset}`} source={source} />)}
      </section>
    </AppShell>
  );
}
