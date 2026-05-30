import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";

export default function MethodologyPage() {
  return (
    <AppShell>
      <PageHeader title="Methodology" subtitle="How indicators become plain-English household pressure signals." />
      <section className="panel page-panel methodology-grid">
        {[
          ["CPI", "Consumer price indexes are translated into year-over-year pressure rather than raw index levels."],
          ["YoY and MoM", "Changes are calculated only when the current and comparison values are available."],
          ["Basket cost", "Selected retail products are multiplied by monthly quantities. It is not the full CPI basket."],
          ["Affordability score", "A 0 to 100 composite using inflation, food, shelter, fuel, and unemployment pressure."],
          ["Leaderboards", "Regions are ranked by latest available observations and calculation direction."],
          ["Freshness", "Latest checked is when the app looked; latest available is the source period released."]
        ].map(([title, body]) => <article key={title}><h2>{title}</h2><p>{body}</p></article>)}
      </section>
    </AppShell>
  );
}
