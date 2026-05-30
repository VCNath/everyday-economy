import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

const entries = [
  ["0.11.0", "Phase 11 public beta readiness", "Added feedback, help, FAQ, known limitations, changelog, release notes, and beta status messaging."],
  ["0.10.0", "Phase 10 N.P.E.M.", "Added the National Personal Economic Model scoring scaffold with scenarios, confidence, provenance, and UI pages."],
  ["0.9.0", "Phase 9 staging readiness", "Prepared deployment docs, staging QA, backup/restore, and security checklists."],
];

export default function ChangelogPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Changelog" title="What changed" body="A simple public history of product, data, and methodology changes." />
      <section className="stack">
        {entries.map(([version, title, body]) => (
          <article className="panel" key={version}>
            <p className="eyebrow">{version}</p>
            <h2>{title}</h2>
            <p>{body}</p>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
