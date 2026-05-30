import Link from "next/link";
import { LayoutDashboard, Map, ShoppingBasket, Trophy, User } from "lucide-react";

const items = [
  ["Dashboard", "/dashboard", LayoutDashboard],
  ["Map", "/map", Map],
  ["Rankings", "/leaderboards", Trophy],
  ["Basket", "/basket", ShoppingBasket],
  ["Account", "/account/profile", User]
] as const;

export function MobileNav() {
  return (
    <nav className="mobile-nav" aria-label="Mobile navigation">
      {items.map(([label, href, Icon]) => (
        <Link key={href} href={href}>
          <Icon size={18} aria-hidden />
          <span>{label}</span>
        </Link>
      ))}
    </nav>
  );
}
