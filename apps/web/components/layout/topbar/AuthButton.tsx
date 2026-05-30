"use client";

import Link from "next/link";
import { UserMenu } from "./UserMenu";
import { useAuth } from "@/hooks/useAuth";

export function AuthButton() {
  const auth = useAuth();
  if (auth.isAuthenticated) {
    return <UserMenu />;
  }
  return (
    <Link className="button primary compact" href="/auth/login">
      Log in
    </Link>
  );
}
