import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemMethodologyNote } from "@/components/npem/NpemMethodologyNote";

export default function HelpMethodologyPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Help" title="Methodology, in plain English" body="Every major number should tell you what changed, where it changed, and how much trust to put in it." />
      <section className="panel">
        <h2>Trust language</h2>
        <p>Latest available means the newest official source release. Estimated means a value uses partial, seeded, or proxy coverage. Cached means the app is showing stored values while a source or backend is unavailable.</p>
      </section>
      <NpemMethodologyNote />
    </AppShell>
  );
}
