import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

const faqs = [
  ["What is Everyday Economy?", "Local cost-of-living intelligence for Canadian regions, built around inflation, groceries, shelter, gas, jobs, baskets, leaderboards, and N.P.E.M."],
  ["What does latest available data mean?", "Most official economic data is released monthly or with a delay. The app shows the newest available release, not second-by-second live data."],
  ["What is CPI?", "The Consumer Price Index tracks how prices change for a basket of goods and services over time."],
  ["What is the basic basket?", "A practical estimate of selected monthly essentials. Some items may be estimated until full source coverage is available."],
  ["What is N.P.E.M.?", "The National Personal Economic Model compares economic pressure and resilience across archetypes using scenario weights, confidence grades, and provenance."],
  ["Why do some values say estimated?", "Estimated labels mean the value uses seeded data, a proxy, or partial coverage. It should be read directionally."],
  ["What does confidence grade mean?", "Confidence combines coverage, recency, directness, reliability, proxy share, and suppression risk."],
  ["Why are some groups overlays?", "Overlay cohorts can overlap with core archetypes, so they are analytical layers rather than mutually exclusive headline groups."],
  ["How do alerts work?", "Alerts watch saved regions for threshold or change conditions and create in-app notifications when triggered."],
  ["How do I report a data issue?", "Use the Feedback button and choose Data issue. The current page path is included automatically."],
];

export default function FaqPage() {
  return (
    <AppShell>
      <PageHero eyebrow="FAQ" title="Questions people ask first" body="Short answers for beta users who want useful context without reading the whole methodology." />
      <section className="stack">
        {faqs.map(([question, answer]) => (
          <article className="panel" key={question}>
            <h2>{question}</h2>
            <p>{answer}</p>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
