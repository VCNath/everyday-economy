import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemGroupSelector } from "@/components/npem/NpemGroupSelector";
import { getNpemGroups, selectNpemGroups } from "@/lib/api-client";

export default async function NpemGroupsPage() {
  const [groups, selected] = await Promise.all([getNpemGroups(), selectNpemGroups({ province: "AB" })]);
  return (
    <AppShell>
      <PageHero eyebrow="N.P.E.M. groups" title="Archetypes and overlays" body="Core archetypes support headline rankings. Overlays are analytical cohorts and may overlap." />
      <NpemGroupSelector groups={groups} />
      <section className="panel">
        <h3>Selected groups for Alberta</h3>
        <pre className="code-block">{JSON.stringify(selected, null, 2)}</pre>
      </section>
    </AppShell>
  );
}
