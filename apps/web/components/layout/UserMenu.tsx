"use client";

import Link from "next/link";
import { User } from "lucide-react";

import { useAuth } from "@/hooks/useAuth";

export function UserMenu() {
  const auth = useAuth();
  if (!auth.isAuthenticated) {
    return (
      <div className="user-menu logged-out">
        <Link href="/auth/login">Log in</Link>
        <Link href="/auth/signup">Create account</Link>
      </div>
    );
  }

  return (
    <div className="user-menu">
      <span className="avatar">
        <User size={16} aria-hidden />
      </span>
      <span>{auth.user?.display_name ?? auth.user?.email ?? "Account"}</span>
      <Link href="/account/profile">Profile</Link>
      <Link href="/account/saved-regions">Saved Regions</Link>
      <button className="button" type="button" onClick={() => auth.logout()}>Log out</button>
    </div>
  );
}
