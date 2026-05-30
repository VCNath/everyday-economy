"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { useAuth } from "@/hooks/useAuth";
import { getNotifications, getSavedRegions, getUnreadNotificationCount } from "@/lib/api-client";

export function PersonalAlertsPanel() {
  const auth = useAuth();
  const [unread, setUnread] = useState(0);
  const [savedCount, setSavedCount] = useState(0);
  const [latest, setLatest] = useState<string | null>(null);

  useEffect(() => {
    if (!auth.token) return;
    Promise.all([getUnreadNotificationCount(auth.token), getSavedRegions(auth.token), getNotifications(auth.token)])
      .then(([count, saved, notes]) => {
        setUnread(count);
        setSavedCount(saved.length);
        setLatest(notes[0]?.title ?? null);
      });
  }, [auth.token]);

  if (!auth.isAuthenticated) {
    return (
      <section className="panel">
        <h3>Personal Layer</h3>
        <p>Create an account to save regions and get alerts.</p>
        <Link className="button primary" href="/auth/signup">Create account</Link>
      </section>
    );
  }

  return (
    <section className="panel">
      <h3>Watchlist Alerts</h3>
      <p>Saved regions: {savedCount} · Unread notifications: {unread}</p>
      <p>Latest: {latest ?? "No notifications yet"}</p>
      <div className="row">
        <Link className="button" href="/account/alerts">Manage alerts</Link>
        <Link className="button" href="/account/notifications">Open inbox</Link>
        <Link className="button" href="/account/reports">Monthly reports</Link>
      </div>
    </section>
  );
}

