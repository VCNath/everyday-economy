"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { generateMonthlyReport, getAlertRules, getWatchlist, removeSavedRegion } from "@/lib/api-client";
import type { WatchlistRegion } from "@/lib/types";

export default function SavedRegionsPage() {
  const auth = useAuth();
  const [rows, setRows] = useState<WatchlistRegion[]>([]);
  const [loading, setLoading] = useState(true);
  const [alertsByLocation, setAlertsByLocation] = useState<Record<string, number>>({});

  useEffect(() => {
    if (!auth.token) {
      setLoading(false);
      return;
    }
    Promise.all([getWatchlist(auth.token), getAlertRules(auth.token)])
      .then(([watchlist, alerts]) => {
        setRows(watchlist);
        const counts: Record<string, number> = {};
        for (const alert of alerts) {
          counts[alert.location_id] = (counts[alert.location_id] ?? 0) + 1;
        }
        setAlertsByLocation(counts);
      })
      .finally(() => setLoading(false));
  }, [auth.token]);

  async function remove(locationId: string) {
    if (!auth.token) return;
    await removeSavedRegion(auth.token, locationId);
    setRows((current) => current.filter((row) => row.location_id !== locationId));
  }

  return (
    <AppShell>
      <PageHeader title="Saved Regions" subtitle="Your personal economic watchlist." />
      {!auth.isAuthenticated ? (
        <EmptyState title="Sign in to view your watchlist" body="Save provinces or cities to build your personal economic watchlist." action="Log in" href="/auth/login" />
      ) : loading ? (
        <section className="panel">Loading saved regions...</section>
      ) : rows.length === 0 ? (
        <EmptyState title="No saved regions yet" body="Save provinces or cities to build your personal economic watchlist." action="Explore Map" href="/map" />
      ) : (
        <section className="stack">
          {rows.map((row) => (
            <article key={row.location_id} className="panel">
              <div className="row">
                <strong>{row.name}</strong>
                <div className="row">
                  <Link className="button" href={`/account/alerts?location=${row.location_id}`}>Create alert</Link>
                  <button className="button" type="button" onClick={async () => { if (!auth.token) return; await generateMonthlyReport(auth.token, row.location_id); }}>Generate report</button>
                  <button className="button" type="button" onClick={() => remove(row.location_id)}>Remove</button>
                </div>
              </div>
              <p>CPI: {row.summary.cpi_yoy?.toFixed(1)}% | Food: {row.summary.food_cpi_yoy?.toFixed(1)}% | Gas: {row.summary.gas_price_cents_litre?.toFixed(1)}¢/L</p>
              <p>Unemployment: {row.summary.unemployment_rate?.toFixed(1)}% | Basket: ${row.summary.basic_basket_monthly_cost?.toFixed(2)} | Affordability: {row.summary.affordability_score?.toFixed(1)}</p>
              <small>Status: {row.freshness.freshness_status} · Latest: {row.freshness.latest_period ?? "n/a"} · Active alerts: {alertsByLocation[row.location_id] ?? 0}</small>
            </article>
          ))}
        </section>
      )}
    </AppShell>
  );
}
