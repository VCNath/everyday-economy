"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useAuth } from "@/hooks/useAuth";

export function AuthCard({ mode }: { mode: "login" | "signup" | "forgot" | "reset" }) {
  const isSignup = mode === "signup";
  const auth = useAuth();
  const title = isSignup
    ? "Create your account"
    : mode === "forgot" || mode === "reset"
      ? "Reset your password"
      : "Everyday Economy";
  const subtitle = isSignup
    ? "Save regions, baskets, and alerts."
    : mode === "forgot" || mode === "reset"
      ? "Recover access to your saved regions and alerts."
      : "Sign in to save regions and preferences.";
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit() {
    setSubmitting(true);
    setMessage(null);
    setError(null);
    try {
      if (mode === "forgot") {
        const result = await auth.forgotPassword(email);
        if (!result.ok) {
          setError(result.error ?? "Could not send reset email.");
          return;
        }
        setMessage("Password reset email sent if the account exists.");
        return;
      }
      if (mode === "reset") {
        if (!password || password !== confirm) {
          setError("Passwords must match.");
          return;
        }
        const result = await auth.resetPassword(password);
        if (!result.ok) {
          setError(result.error ?? "Could not reset password.");
          return;
        }
        setMessage("Password updated.");
        return;
      }
      const result = isSignup
        ? await auth.signup(name, email, password)
        : await auth.login(email, password);
      if (!result.ok) {
        setError(result.error ?? "Could not sign you in.");
        return;
      }
      router.push("/dashboard");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card panel">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        {isSignup ? <label className="field"><span>Name</span><input value={name} onChange={(event) => setName(event.target.value)} /></label> : null}
        <label className="field"><span>Email</span><input type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label>
        {mode !== "forgot" ? <label className="field"><span>Password</span><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label> : null}
        {mode === "reset" ? <label className="field"><span>Confirm password</span><input type="password" value={confirm} onChange={(event) => setConfirm(event.target.value)} /></label> : null}
        {error ? <p className="status error">{error}</p> : null}
        {message ? <p className="status">{message}</p> : null}
        <button className="button primary" type="button" disabled={submitting} onClick={onSubmit}>{submitting ? "Working..." : isSignup ? "Create account" : mode === "forgot" ? "Send reset link" : mode === "reset" ? "Reset password" : "Sign in"}</button>
        <button className="button" type="button" disabled>Continue with Google - coming soon</button>
        <div className="auth-links">
          <Link href="/auth/forgot-password">Forgot password?</Link>
          <Link href={isSignup ? "/auth/login" : "/auth/signup"}>{isSignup ? "Already have an account?" : "New here? Create account"}</Link>
        </div>
      </section>
    </main>
  );
}
