import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemScenarioDeltaTable } from "@/components/npem/NpemScenarioDeltaTable";
import { compareNpemScenarios } from "@/lib/api-client";

export default async function NpemComparePage() {
  const deltas = await compareNpemScenarios({ province: "AB", scenario_a: "baseline", scenario_b: "housing_stress" });
  return (
    <AppShell>
      <PageHero eyebrow="N.P.E.M. compare" title="Scenario comparison" body="See how archetype rankings move when housing stress or income strength assumptions change." />
      <NpemScenarioDeltaTable rows={deltas} />
    </AppShell>
  );
}
