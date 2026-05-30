"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Lock } from "lucide-react";

import { navigationIcons, type NavigationItem } from "@/lib/navigation";

export function SidebarItem({ item, isAuthenticated }: { item: NavigationItem; isAuthenticated: boolean }) {
  const pathname = usePathname();
  const Icon = navigationIcons[item.icon];
  const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
  const locked = Boolean(item.authRequired && !isAuthenticated);

  return (
    <Link className={`sidebar-item ${active ? "active" : ""} ${locked ? "locked" : ""}`} href={locked ? "/auth/login" : item.href}>
      <Icon size={18} aria-hidden />
      <span>{item.label}</span>
      {item.badge ? <b>{item.badge}</b> : null}
      {locked ? <Lock className="sidebar-lock" size={14} aria-label="Login required" /> : null}
    </Link>
  );
}
