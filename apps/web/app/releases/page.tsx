import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

export default function ReleasesPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Release notes" title="Public beta release notes" body="Notes for testers about what is ready, what is estimated, and what needs feedback." />
      <section className="panel">
        <p className="eyebrow">2026-05-29 · v0.11.0-beta</p>
        <h2>Public beta preparation</h2>
        <ul className="clean-list">
          <li>Added in-app feedback and admin feedback review.</li>
          <li>Added help, FAQ, known limitations, changelog, and release notes pages.</li>
          <li>Added beta status messaging across the app.</li>
          <li>N.P.E.M. remains demo/estimated until source-backed adapters are complete.</li>
          <li>Known issue: production deployment URLs and monitoring providers are still environment-specific setup tasks.</li>
        </ul>
      </section>
    </AppShell>
  );
}
