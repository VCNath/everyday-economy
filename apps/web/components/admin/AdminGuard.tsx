"use client";

import { EmptyState } from "@/components/ui/EmptyState";
import { useAuth } from "@/hooks/useAuth";

export function AdminGuard({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  if (!auth.isAuthenticated) {
    return <EmptyState title="Admin sign-in required" body="Log in with an admin account to access operations pages." action="Log in" href="/auth/login" />;
  }
  if (!auth.isAdmin) {
    return <EmptyState title="Forbidden" body="Your account is authenticated but does not have admin access." />;
  }
  return <>{children}</>;
}

