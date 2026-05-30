"use client";

import type { AuthState, User } from "@/lib/types";

const AUTH_TOKEN_KEY = "ee_auth_token";
const AUTH_NAME_KEY = "ee_auth_name";

function canUseWindow() {
  return typeof window !== "undefined";
}

export function buildDemoToken(email: string, displayName?: string) {
  const cleanEmail = email.trim().toLowerCase();
  const cleanName = (displayName ?? "").trim();
  return cleanName ? `demo:${cleanEmail}:${cleanName}` : `demo:${cleanEmail}`;
}

export function isDemoAuthEnabled() {
  return process.env.NEXT_PUBLIC_ALLOW_DEMO_AUTH === "true" || !process.env.NEXT_PUBLIC_SUPABASE_URL;
}

export function persistAuthToken(token: string, displayName?: string) {
  if (!canUseWindow()) return;
  window.localStorage.setItem(AUTH_TOKEN_KEY, token);
  if (displayName) window.localStorage.setItem(AUTH_NAME_KEY, displayName);
}

export function clearAuthToken() {
  if (!canUseWindow()) return;
  window.localStorage.removeItem(AUTH_TOKEN_KEY);
  window.localStorage.removeItem(AUTH_NAME_KEY);
}

export function getStoredAuthToken(): string | null {
  if (!canUseWindow()) return null;
  return window.localStorage.getItem(AUTH_TOKEN_KEY);
}

export function getStoredDisplayName(): string | null {
  if (!canUseWindow()) return null;
  return window.localStorage.getItem(AUTH_NAME_KEY);
}

export function decodeDemoUser(token: string): User | null {
  if (!token.startsWith("demo:")) return null;
  const raw = token.replace("demo:", "");
  const [email, displayName, explicitRole] = raw.split(":");
  if (!email) return null;
  const role = explicitRole === "admin" || explicitRole === "user"
    ? explicitRole
    : email.endsWith("@admin.local")
      ? "admin"
      : "user";
  return {
    id: `demo-${email}`,
    email,
    display_name: displayName || undefined,
    role,
    avatar_url: null
  };
}

export function emptyAuthState(): AuthState {
  return {
    loading: false,
    isAuthenticated: false,
    isAdmin: false,
    token: null,
    user: null
  };
}
