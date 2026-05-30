import Link from "next/link";
import { BarChart3, CalendarDays, MapPin, Search } from "lucide-react";

import { metricOptions } from "@/lib/constants";
import { DataFreshnessBadge } from "@/components/cards/DataFreshnessBadge";

export function Header() {
  return (
    <header className="app-header">
      <div className="brand">
        <Link href="/">Everyday Economy</Link>
        <span className="brand-subtitle">Economic weather for household life</span>
      </div>
      <div className="header-controls" aria-label="Dashboard filters">
        <label className="search-box">
          <Search size={16} aria-hidden />
          <input placeholder="Search region..." aria-label="Search region" />
        </label>
        <label className="control">
          <MapPin size={16} aria-hidden />
          <select aria-label="Region">
            <option>Canada</option>
            <option>Saskatchewan</option>
            <option>Toronto</option>
          </select>
        </label>
        <label className="control">
          <BarChart3 size={16} aria-hidden />
          <select aria-label="Metric">
            {metricOptions.map((metric) => (
              <option key={metric.id}>{metric.label}</option>
            ))}
          </select>
        </label>
        <label className="control">
          <CalendarDays size={16} aria-hidden />
          <select aria-label="Period">
            <option>Latest</option>
            <option>1M</option>
            <option>3M</option>
            <option>12M</option>
          </select>
        </label>
        <DataFreshnessBadge period="Apr 2026" />
        <Link className="methodology-link" href="/methodology">
          Methodology
        </Link>
      </div>
    </header>
  );
}
