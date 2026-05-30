import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";

export default function BillingPage() {
  return (
    <AppShell>
      <PageHeader title="Billing" subtitle="Prepared for future paid plans and advanced alerts." />
      <EmptyState title="No billing yet" body="The MVP is public and free. Paid plan scaffolding is ready behind feature flags." />
    </AppShell>
  );
}
