"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { getCurrentUser } from "@/lib/api-client";
import { buildDemoToken, clearAuthToken, decodeDemoUser, emptyAuthState, getStoredAuthToken, isDemoAuthEnabled, persistAuthToken } from "@/lib/auth";
import { getSupabaseBrowserClient } from "@/lib/supabase";
import type { AuthState, User } from "@/lib/types";

type AuthContextValue = AuthState & {
  login: (email: string, password: string, displayName?: string) => Promise<{ ok: boolean; error?: string }>;
  signup: (name: string, email: string, password: string) => Promise<{ ok: boolean; error?: string }>;
  forgotPassword: (email: string) => Promise<{ ok: boolean; error?: string }>;
  resetPassword: (password: string) => Promise<{ ok: boolean; error?: string }>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({ ...emptyAuthState(), loading: true });

  async function loginUser(email: string, password: string, displayName?: string) {
    const supabase = getSupabaseBrowserClient();
    if (supabase) {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) return { ok: false, error: error.message };
      const token = data.session?.access_token;
      if (!token) return { ok: false, error: "Could not establish a Supabase session." };
      const user = await getCurrentUser(token);
      setState({ loading: false, isAuthenticated: true, isAdmin: user.role === "admin", token, user });
      return { ok: true };
    }
    if (!isDemoAuthEnabled()) return { ok: false, error: "Authentication provider is not configured." };
    const token = buildDemoToken(email, displayName);
    persistAuthToken(token, displayName);
    let user: User | null = null;
    try {
      user = await getCurrentUser(token);
    } catch {
      user = decodeDemoUser(token);
    }
    if (!user) return { ok: false, error: "Could not establish a session." };
    setState({
      loading: false,
      isAuthenticated: true,
      isAdmin: user.role === "admin",
      token,
      user
    });
    return { ok: true };
  }

  useEffect(() => {
    const supabase = getSupabaseBrowserClient();
    if (supabase) {
      supabase.auth.getSession().then(async ({ data }) => {
        const token = data.session?.access_token;
        if (!token) {
          setState(emptyAuthState());
          return;
        }
        try {
          const user = await getCurrentUser(token);
          setState({ loading: false, token, user, isAuthenticated: true, isAdmin: user.role === "admin" });
        } catch {
          setState(emptyAuthState());
        }
      });
      const { data: subscription } = supabase.auth.onAuthStateChange(async (_event, session) => {
        const token = session?.access_token;
        if (!token) {
          setState(emptyAuthState());
          return;
        }
        try {
          const user = await getCurrentUser(token);
          setState({ loading: false, token, user, isAuthenticated: true, isAdmin: user.role === "admin" });
        } catch {
          setState(emptyAuthState());
        }
      });
      return () => subscription.subscription.unsubscribe();
    }

    const token = getStoredAuthToken();
    if (!token) {
      setState(emptyAuthState());
      return;
    }
    const fallbackUser = decodeDemoUser(token);
    getCurrentUser(token)
      .then((user) => {
        setState({
          loading: false,
          token,
          user,
          isAuthenticated: true,
          isAdmin: user.role === "admin"
        });
      })
      .catch(() => {
        if (fallbackUser) {
          setState({
            loading: false,
            token,
            user: fallbackUser,
            isAuthenticated: true,
            isAdmin: fallbackUser.role === "admin"
          });
          return;
        }
        clearAuthToken();
        setState(emptyAuthState());
      });
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      async login(email: string, _password: string, displayName?: string) {
        return loginUser(email, _password, displayName);
      },
      async signup(name: string, email: string, password: string) {
        const supabase = getSupabaseBrowserClient();
        if (supabase) {
          const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: { data: { display_name: name } },
          });
          if (error) return { ok: false, error: error.message };
          const token = data.session?.access_token;
          if (!token) return { ok: true };
          const user = await getCurrentUser(token);
          setState({ loading: false, isAuthenticated: true, isAdmin: user.role === "admin", token, user });
          return { ok: true };
        }
        if (!isDemoAuthEnabled()) return { ok: false, error: "Authentication provider is not configured." };
        return loginUser(email, password, name);
      },
      async forgotPassword(email: string) {
        const supabase = getSupabaseBrowserClient();
        if (!supabase) return { ok: false, error: "Password reset requires Supabase configuration." };
        const redirectTo = `${window.location.origin}/auth/reset-password`;
        const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo });
        return error ? { ok: false, error: error.message } : { ok: true };
      },
      async resetPassword(password: string) {
        const supabase = getSupabaseBrowserClient();
        if (!supabase) return { ok: false, error: "Password reset requires Supabase configuration." };
        const { error } = await supabase.auth.updateUser({ password });
        return error ? { ok: false, error: error.message } : { ok: true };
      },
      async logout() {
        const supabase = getSupabaseBrowserClient();
        if (supabase) await supabase.auth.signOut();
        clearAuthToken();
        setState(emptyAuthState());
      }
    }),
    [state]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error("useAuthContext must be used within AuthProvider.");
  }
  return value;
}
