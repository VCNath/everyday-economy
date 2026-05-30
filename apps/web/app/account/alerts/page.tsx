"use client";

import { useEffect, useState } from "react";

import { AlertRuleForm } from "@/components/alerts/AlertRuleForm";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { createAlertRule, deleteAlertRule, disableAlertRule, enableAlertRule, getAlertRules } from "@/lib/api-client";
import type { AlertRule } from "@/lib/types";

export default function AlertsPage() {
  const auth = useAuth();
  const [rules, setRules] = useState<AlertRule[]>([]);

  async function refresh() {
    if (!auth.token) return;
    setRules(await getAlertRules(auth.token));
  }

  useEffect(() => { void refresh(); }, [auth.token]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!auth.isAuthenticated) {
    return (
      <AppShell>
        <PageHeader title="Alerts" subtitle="Create threshold alerts for your saved regions." />
        <EmptyState title="Sign in to create alerts" body="Track inflation, groceries, gas, jobs, and affordability with personal alert rules." action="Log in" href="/auth/login" />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Alerts" subtitle="Manage alert rules tied to your saved regions." />
      <AlertRuleForm onSubmit={async (payload) => { if (!auth.token) return; await createAlertRule(auth.token, payload); await refresh(); }} />
      {rules.length === 0 ? (
        <EmptyState title="No alerts yet" body="Create an alert to watch inflation, groceries, gas, jobs, or affordability in your saved regions." />
      ) : (
        <section className="stack">
          {rules.map((rule) => (
            <article className="panel" key={rule.id}>
              <div className="row">
                <strong>{rule.location_name} · {rule.indicator_name}</strong>
                <div className="row">
                  <button className="button" type="button" onClick={async () => { if (!auth.token) return; await (rule.enabled ? disableAlertRule(auth.token, rule.id) : enableAlertRule(auth.token, rule.id)); await refresh(); }}>{rule.enabled ? "Disable" : "Enable"}</button>
                  <button className="button" type="button" onClick={async () => { if (!auth.token) return; await deleteAlertRule(auth.token, rule.id); await refresh(); }}>Delete</button>
                </div>
              </div>
              <p>{rule.comparison_operator} {rule.threshold_value ?? rule.change_value ?? rule.rank_value ?? "—"} · {rule.enabled ? "Enabled" : "Disabled"}</p>
            </article>
          ))}
        </section>
      )}
    </AppShell>
  );
}

