import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemMethodologyNote } from "@/components/npem/NpemMethodologyNote";

export default function NpemMethodologyPage() {
  return (
    <AppShell>
      <PageHero eyebrow="N.P.E.M. methodology" title="Transparent scoring, cautious cohorts" body="N.P.E.M. is a model layer, not a claim that every variable is directly observed for every group." />
      <NpemMethodologyNote />
      <section className="panel">
        <h3>Core Rules</h3>
        <ul className="clean-list">
          <li>Normalize components from 0 to 100.</li>
          <li>Invert burden metrics so higher score means stronger position.</li>
          <li>Use scenario weights that sum to 1.00.</li>
          <li>Carry confidence and provenance with every score.</li>
          <li>Label overlays as overlapping cohorts.</li>
          <li>Reduce confidence or suppress output when small-cell risk is high.</li>
        </ul>
      </section>
    </AppShell>
  );
}
