import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";

export default function TrendsPage() {
  return (
    <AppShell>
      <PageHeader title="Trends" subtitle="Historical movement across regions and indicators." />
      <EmptyState title="Trend explorer is coming soon" body="Historical charts are scaffolded and ready for source-backed series." />
    </AppShell>
  );
}
