import Link from "next/link";

import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";

const links = [
  ["/help/faq", "FAQ", "Plain answers about data, scoring, alerts, and saved regions."],
  ["/help/methodology", "Methodology", "How latest available data, baskets, leaderboards, and N.P.E.M. are explained."],
  ["/help/data-sources", "Data sources", "Where numbers come from and how freshness is tracked."],
  ["/help/known-limitations", "Known limitations", "What is estimated, partial, cached, or still in beta."],
];

export default function HelpPage() {
  return (
    <AppShell>
      <PageHero eyebrow="Help" title="Use Everyday Economy with confidence" body="Quick explanations for the public beta: what the numbers mean, where they come from, and how to report problems." />
      <section className="content-grid two">
        {links.map(([href, title, body]) => (
          <Link className="panel help-card" href={href} key={href}>
            <h2>{title}</h2>
            <p>{body}</p>
          </Link>
        ))}
      </section>
    </AppShell>
  );
}
