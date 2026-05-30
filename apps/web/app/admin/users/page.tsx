"use client";

import { useEffect, useState } from "react";

import { AdminGuard } from "@/components/admin/AdminGuard";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuth } from "@/hooks/useAuth";
import { getAdminUsers } from "@/lib/api-client";
import type { AdminUserRow } from "@/lib/types";

export default function UsersPage() {
  const auth = useAuth();
  const [users, setUsers] = useState<AdminUserRow[]>([]);
  useEffect(() => {
    if (!auth.token) return;
    getAdminUsers(auth.token).then(setUsers);
  }, [auth.token]);
  return (
    <AppShell>
      <PageHeader title="Users" subtitle="Admin user management scaffold." />
      <AdminGuard>
        <section className="panel page-panel">
          <table className="compact-table">
            <thead><tr><th>Email</th><th>Name</th><th>Role</th><th>Saved</th><th>Alerts</th><th>Notifications</th></tr></thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.email}</td>
                  <td>{user.display_name ?? "-"}</td>
                  <td>{user.role}</td>
                  <td>{user.saved_region_count}</td>
                  <td>{user.alert_rule_count}</td>
                  <td>{user.notification_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </AdminGuard>
    </AppShell>
  );
}
