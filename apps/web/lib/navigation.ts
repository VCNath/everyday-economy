import {
  Activity,
  AlertTriangle,
  Bell,
  BookOpen,
  Bookmark,
  Database,
  Flag,
  GitCompare,
  LayoutDashboard,
  Lock,
  Map,
  MapPinned,
  MessageSquare,
  Settings2,
  ShoppingBasket,
  SlidersHorizontal,
  Sparkles,
  ScrollText,
  TrendingUp,
  Trophy,
  User,
  Users,
  FileText
} from "lucide-react";

export type NavigationItem = {
  label: string;
  href: string;
  icon: keyof typeof navigationIcons;
  authRequired?: boolean;
  adminOnly?: boolean;
  disabled?: boolean;
  badge?: string;
};

export type NavigationSection = {
  section: string;
  items: NavigationItem[];
};

export const navigationIcons = {
  Activity,
  AlertTriangle,
  Bell,
  BookOpen,
  Bookmark,
  Database,
  Flag,
  GitCompare,
  LayoutDashboard,
  Lock,
  Map,
  MapPinned,
  MessageSquare,
  Settings2,
  ShoppingBasket,
  SlidersHorizontal,
  Sparkles,
  ScrollText,
  TrendingUp,
  Trophy,
  User,
  Users,
  FileText
};

export const navigation: NavigationSection[] = [
  {
    section: "Main",
    items: [
      { label: "Dashboard", href: "/dashboard", icon: "LayoutDashboard" },
      { label: "Map Explorer", href: "/map", icon: "Map" },
      { label: "Leaderboards", href: "/leaderboards", icon: "Trophy" },
      { label: "Compare", href: "/compare", icon: "GitCompare" },
      { label: "Basket Builder", href: "/basket", icon: "ShoppingBasket" }
    ]
  },
  {
    section: "Intelligence",
    items: [
      { label: "Insights", href: "/insights", icon: "Sparkles" },
      { label: "Region Profiles", href: "/regions", icon: "MapPinned" },
      { label: "N.P.E.M.", href: "/npem", icon: "Activity" },
      { label: "Trends", href: "/trends", icon: "TrendingUp", badge: "Soon" }
    ]
  },
  {
    section: "Data",
    items: [
      { label: "Sources", href: "/data/sources", icon: "Database" },
      { label: "Methodology", href: "/data/methodology", icon: "BookOpen" },
      { label: "API Status", href: "/data/api-status", icon: "Activity" }
    ]
  },
  {
    section: "Account",
    items: [
      { label: "Saved Regions", href: "/account/saved-regions", icon: "Bookmark", authRequired: true },
      { label: "Alerts", href: "/account/alerts", icon: "Bell", authRequired: true },
      { label: "Notifications", href: "/account/notifications", icon: "Activity", authRequired: true },
      { label: "Monthly Reports", href: "/account/reports", icon: "FileText", authRequired: true },
      { label: "Preferences", href: "/account/preferences", icon: "SlidersHorizontal", authRequired: true },
      { label: "Profile", href: "/account/profile", icon: "User", authRequired: true }
    ]
  },
  {
    section: "Admin",
    items: [
      { label: "Data Ingestion", href: "/admin/data-ingestion", icon: "Database", adminOnly: true },
      { label: "Admin Overview", href: "/admin", icon: "LayoutDashboard", adminOnly: true },
      { label: "Source Health", href: "/admin/source-health", icon: "Activity", adminOnly: true },
      { label: "Data Quality", href: "/admin/data-quality", icon: "AlertTriangle", adminOnly: true },
      { label: "Users", href: "/admin/users", icon: "Users", adminOnly: true },
      { label: "Feature Flags", href: "/admin/feature-flags", icon: "Flag", adminOnly: true },
      { label: "N.P.E.M. Ops", href: "/admin/npem", icon: "Activity", adminOnly: true },
      { label: "Feedback", href: "/admin/feedback", icon: "MessageSquare", adminOnly: true },
      { label: "Audit Logs", href: "/admin/audit-logs", icon: "ScrollText", adminOnly: true }
    ]
  }
];
