import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

export default function HelpDataSourcesPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Help" title="Data sources and freshness" body="Everyday Economy favours official public sources and labels source freshness clearly." />
      <section className="content-grid two">
        <article className="panel"><h2>Statistics Canada</h2><p>Backbone source for CPI, food, shelter, gasoline, labour, population, and future N.P.E.M. variables.</p></article>
        <article className="panel"><h2>Bank of Canada</h2><p>Financial context for rates, exchange rates, and future debt/rate overlays.</p></article>
        <article className="panel"><h2>CMHC, CRA, CIHI</h2><p>Planned or cautious sources for housing, direct tax parameters, and health expenditure structure.</p></article>
        <article className="panel"><h2>Freshness</h2><p>Source status shows latest period, last checked time, stale/error states, and notes when data is partial.</p></article>
      </section>
    </AppShell>
  );
}
