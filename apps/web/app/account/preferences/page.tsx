"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { Select } from "@/components/ui/Select";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { getNotificationPreferences, getUserPreferences, updateNotificationPreferences, updateUserPreferences } from "@/lib/api-client";
import type { UserPreferences } from "@/lib/types";

export default function PreferencesPage() {
  const auth = useAuth();
  const [preferences, setPreferences] = useState<UserPreferences>({
    default_location_id: "CA",
    default_metric: "cpi_all_items_yoy",
    default_period: "latest",
    default_basket_id: "basic",
    household_size: 1,
    theme: "system",
    data_density: "simple"
  });
  const [status, setStatus] = useState<string | null>(null);
  const [notificationPreferences, setNotificationPreferences] = useState({
    in_app_enabled: true,
    email_enabled: false,
    monthly_report_enabled: true,
    data_release_alerts_enabled: true,
    source_health_alerts_enabled: false
  });

  useEffect(() => {
    if (!auth.token) return;
    Promise.all([getUserPreferences(auth.token), getNotificationPreferences(auth.token)]).then(([result, notification]) => {
      setPreferences((current) => ({
        ...current,
        ...result,
        default_location_id: result.default_location_id ?? current.default_location_id ?? "CA",
        default_metric: result.default_metric ?? current.default_metric ?? "cpi_all_items_yoy",
        default_period: result.default_period ?? current.default_period ?? "latest",
        default_basket_id: result.default_basket_id ?? current.default_basket_id ?? "basic"
      }));
      setNotificationPreferences(notification);
    });
  }, [auth.token]);

  async function savePreferences() {
    if (!auth.token) return;
    const [result, notification] = await Promise.all([
      updateUserPreferences(auth.token, preferences),
      updateNotificationPreferences(auth.token, notificationPreferences)
    ]);
    setPreferences((current) => ({
      ...current,
      ...result,
      default_location_id: result.default_location_id ?? current.default_location_id ?? "CA",
      default_metric: result.default_metric ?? current.default_metric ?? "cpi_all_items_yoy",
      default_period: result.default_period ?? current.default_period ?? "latest",
      default_basket_id: result.default_basket_id ?? current.default_basket_id ?? "basic"
    }));
    setNotificationPreferences(notification);
    setStatus("Preferences saved.");
  }

  return (
    <AppShell>
      <PageHeader title="Preferences" subtitle="Default region, metric, period, basket, household size, and theme." />
      {!auth.isAuthenticated ? (
        <EmptyState title="Sign in to edit preferences" body="Your defaults are saved to your account after login." action="Log in" href="/auth/login" />
      ) : (
        <section className="panel preference-grid">
          <Select label="Default region" options={["CA", "CA-SK", "CA-AB", "CA-MB"]} value={preferences.default_location_id ?? "CA"} onChange={(value) => setPreferences((current) => ({ ...current, default_location_id: value }))} />
          <Select label="Default map metric" options={["cpi_all_items_yoy", "cpi_food_yoy", "gas_regular_cents_litre", "affordability_score"]} value={preferences.default_metric ?? "cpi_all_items_yoy"} onChange={(value) => setPreferences((current) => ({ ...current, default_metric: value }))} />
          <Select label="Default period" options={["latest", "yoy", "mom"]} value={preferences.default_period ?? "latest"} onChange={(value) => setPreferences((current) => ({ ...current, default_period: value }))} />
          <Select label="Basket type" options={["basic", "student", "family", "commuter"]} value={preferences.default_basket_id ?? "basic"} onChange={(value) => setPreferences((current) => ({ ...current, default_basket_id: value }))} />
          <Select label="Household size" options={["1", "2", "4"]} value={String(preferences.household_size)} onChange={(value) => setPreferences((current) => ({ ...current, household_size: Number(value) }))} />
          <Select label="Theme" options={["system", "light", "dark"]} value={preferences.theme} onChange={(value) => setPreferences((current) => ({ ...current, theme: value }))} />
          <Select label="Data density" options={["simple", "detailed"]} value={preferences.data_density} onChange={(value) => setPreferences((current) => ({ ...current, data_density: value }))} />
          <label className="field"><span>In-app notifications</span><input type="checkbox" checked={notificationPreferences.in_app_enabled} onChange={(event) => setNotificationPreferences((current) => ({ ...current, in_app_enabled: event.target.checked }))} /></label>
          <label className="field"><span>Email notifications</span><input type="checkbox" checked={notificationPreferences.email_enabled} disabled onChange={(event) => setNotificationPreferences((current) => ({ ...current, email_enabled: event.target.checked }))} /></label>
          <label className="field"><span>Monthly reports</span><input type="checkbox" checked={notificationPreferences.monthly_report_enabled} onChange={(event) => setNotificationPreferences((current) => ({ ...current, monthly_report_enabled: event.target.checked }))} /></label>
          <label className="field"><span>Data release alerts</span><input type="checkbox" checked={notificationPreferences.data_release_alerts_enabled} onChange={(event) => setNotificationPreferences((current) => ({ ...current, data_release_alerts_enabled: event.target.checked }))} /></label>
          <label className="field"><span>Source health alerts</span><input type="checkbox" checked={notificationPreferences.source_health_alerts_enabled} onChange={(event) => setNotificationPreferences((current) => ({ ...current, source_health_alerts_enabled: event.target.checked }))} /></label>
          <button className="button primary" type="button" onClick={savePreferences}>Save preferences</button>
          {status ? <p>{status}</p> : null}
        </section>
      )}
    </AppShell>
  );
}
