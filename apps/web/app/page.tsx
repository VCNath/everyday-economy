import Link from "next/link";
import Image from "next/image";
import { ArrowRight, Bell, Database, GitCompare, Map, ShieldCheck, ShoppingBasket, Trophy, type LucideIcon } from "lucide-react";

import { getLeaderboard, getMapFeatures } from "@/lib/api-client";
import { EconomicMap } from "@/components/map/EconomicMap";
import { LeaderboardTable } from "@/components/leaderboard/LeaderboardTable";
import { SectionHeader } from "@/components/ui/SectionHeader";

export default async function LandingPage() {
  const [features, rows] = await Promise.all([getMapFeatures(), getLeaderboard("grocery_basket")]);

  return (
    <main className="public-page">
      <header className="public-nav">
        <Link href="/" className="public-brand">Everyday Economy</Link>
        <nav>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/leaderboards">Leaderboards</Link>
          <Link href="/data/methodology">Methodology</Link>
          <Link href="/help">Help</Link>
        </nav>
      </header>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Map-first economic clarity</p>
          <h1>Track the economy where life happens.</h1>
          <p>
            Everyday Economy turns inflation, groceries, gas, jobs, and affordability data into clear local signals.
          </p>
          <div className="hero-actions">
            <Link className="button primary" href="/dashboard">Open Dashboard <ArrowRight size={16} /></Link>
            <Link className="button" href="/leaderboards">View Leaderboards</Link>
          </div>
          <div className="hero-proof">
            <span><ShieldCheck size={15} aria-hidden /> Official sources</span>
            <span><Bell size={15} aria-hidden /> Saved-region alerts</span>
            <span><Database size={15} aria-hidden /> Freshness tracked</span>
          </div>
        </div>
        <div className="hero-art" aria-hidden>
          <Image src="/brand/economic-radar-glass.png" alt="" fill priority sizes="(max-width: 980px) 100vw, 55vw" />
        </div>
        <div className="hero-preview glass-float">
          <EconomicMap features={features} />
        </div>
      </section>
      <section className="landing-section">
        <SectionHeader
          eyebrow="Why it matters"
          title="A dashboard built around household pressure."
          body="The app translates economic data into practical local signals instead of asking people to decode tables."
        />
      </section>
      <section className="feature-grid">
        {([
          [Map, "Map Explorer", "See where household pressure is moving fastest."],
          [Trophy, "Leaderboards", "Find the highest, lowest, and fastest-moving regions."],
          [ShoppingBasket, "Basket Builder", "Translate product prices into a monthly essentials estimate."],
          [GitCompare, "Compare Regions", "Put provinces and cities side by side."],
          [Bell, "Alerts and Reports", "Watch saved regions and get notified when conditions change."],
          [Database, "Source Trust", "Show latest periods, checks, and methodology."]
        ] as Array<[LucideIcon, string, string]>).map(([Icon, title, body]) => (
          <article className="panel" key={String(title)}>
            <Icon size={22} />
            <h2>{title}</h2>
            <p>{body}</p>
          </article>
        ))}
      </section>
      <section className="landing-split">
        <article className="panel landing-leaderboard">
          <SectionHeader eyebrow="Economic standings" title="Leaderboards that invite comparison." body="See which regions are rising fastest, improving, or carrying the most cost pressure." />
          <LeaderboardTable rows={rows.slice(0, 5)} />
        </article>
        <article className="panel landing-preview-card">
          <p className="eyebrow">Human layer</p>
          <h2>Build a basket, save a region, watch the signals.</h2>
          <p>Basket estimates, saved-region watchlists, alerts, and monthly reports bring the data closer to everyday decisions.</p>
          <Link className="button primary" href="/basket">Open Basket Builder <ArrowRight size={16} /></Link>
        </article>
      </section>
      <section className="landing-cta">
        <h2>Ready to scan the local economy?</h2>
        <p>Open the dashboard and see where pressure is changing across Canada.</p>
        <Link className="button primary" href="/dashboard">Open Dashboard <ArrowRight size={16} /></Link>
      </section>
      <footer className="public-footer">Sources: Statistics Canada, Bank of Canada, World Bank, OECD.</footer>
    </main>
  );
}
