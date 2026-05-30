import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

const limitations = [
  "Economic data is latest available, not live second-by-second.",
  "Some basket values use seeded or estimated fallback data.",
  "N.P.E.M. currently uses deterministic demo/proxy inputs until production source adapters are complete.",
  "Overlay cohorts may overlap and should not be read as mutually exclusive populations.",
  "Indigenous identity overlays require additional governance review before public ranking claims.",
  "Province geometry remains simplified until full map geometry is loaded.",
  "Email delivery may be disabled or console-only in staging.",
];

export default function KnownLimitationsPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Known limitations" title="What beta users should know" body="The app is useful now, but public beta means some data coverage, scoring, and alerts are still being refined." />
      <section className="panel">
        <ul className="clean-list">
          {limitations.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </section>
    </AppShell>
  );
}
