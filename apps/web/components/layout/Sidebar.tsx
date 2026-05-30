"use client";

import Link from "next/link";

import { useAuth } from "@/hooks/useAuth";
import { featureFlags } from "@/lib/feature-flags";
import { navigation } from "@/lib/navigation";
import { SidebarItem } from "./SidebarItem";
import { SidebarSection } from "./SidebarSection";

export function Sidebar() {
  const auth = useAuth();
  const sections = navigation.filter((section) => section.section !== "Admin" || (auth.isAdmin && featureFlags.adminPanel));

  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <Link href="/dashboard" className="sidebar-brand">
        <strong>Everyday Economy</strong>
        <span>Economic clarity, local</span>
      </Link>
      <nav>
        {sections.map((section) => (
          <SidebarSection key={section.section} title={section.section}>
            {section.items
              .filter((item) => !item.adminOnly || auth.isAdmin)
              .map((item) => (
                <SidebarItem key={item.href} item={item} isAuthenticated={auth.isAuthenticated} />
              ))}
          </SidebarSection>
        ))}
      </nav>
    </aside>
  );
}
