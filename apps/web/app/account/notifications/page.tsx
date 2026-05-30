"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { getNotifications, getUnreadNotificationCount, markAllNotificationsRead, markNotificationRead } from "@/lib/api-client";
import type { Notification } from "@/lib/types";

export default function NotificationsPage() {
  const auth = useAuth();
  const [items, setItems] = useState<Notification[]>([]);
  const [unread, setUnread] = useState(0);

  async function refresh() {
    if (!auth.token) return;
    const [rows, count] = await Promise.all([getNotifications(auth.token), getUnreadNotificationCount(auth.token)]);
    setItems(rows);
    setUnread(count);
  }
  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!auth.isAuthenticated) {
    return (
      <AppShell>
        <PageHeader title="Notifications" subtitle="Your alert and report inbox." />
        <EmptyState title="Sign in to view notifications" body="Notifications appear when alert thresholds are crossed or reports are generated." action="Log in" href="/auth/login" />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Notifications" subtitle={`Unread: ${unread}`} />
      <div className="row"><button className="button" type="button" onClick={async () => { if (!auth.token) return; await markAllNotificationsRead(auth.token); await refresh(); }}>Mark all read</button></div>
      {items.length === 0 ? (
        <EmptyState title="No notifications yet" body="Alert and report notifications will appear here." />
      ) : (
        <section className="stack">
          {items.map((item) => (
            <article className="panel" key={item.id}>
              <div className="row">
                <strong>{item.title}</strong>
                {!item.is_read ? <button className="button" type="button" onClick={async () => { if (!auth.token) return; await markNotificationRead(auth.token, item.id); await refresh(); }}>Mark read</button> : null}
              </div>
              <p>{item.message}</p>
              <small>{item.severity} · {item.freshness_status ?? "n/a"} · {item.created_at}</small>
            </article>
          ))}
        </section>
      )}
    </AppShell>
  );
}

