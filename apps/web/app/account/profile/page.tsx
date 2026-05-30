"use client";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";

export default function ProfilePage() {
  const auth = useAuth();
  return (
    <AppShell>
      <PageHeader title="Profile" subtitle="Account identity and saved dashboard settings." />
      {!auth.isAuthenticated ? (
        <EmptyState title="Sign in to access your profile" body="Your account profile appears once you are logged in." action="Log in" href="/auth/login" />
      ) : (
        <section className="panel">
          <p><strong>Name:</strong> {auth.user?.display_name ?? "Not set"}</p>
          <p><strong>Email:</strong> {auth.user?.email}</p>
          <p><strong>Role:</strong> {auth.user?.role ?? "user"}</p>
          <button className="button" type="button" onClick={() => auth.logout()}>Log out</button>
        </section>
      )}
    </AppShell>
  );
}
