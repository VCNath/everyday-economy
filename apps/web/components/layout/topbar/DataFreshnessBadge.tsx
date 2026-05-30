import { DatabaseZap } from "lucide-react";

export function DataFreshnessBadge() {
  return (
    <span className="topbar-freshness">
      <DatabaseZap size={15} aria-hidden />
      Updated May 2026
    </span>
  );
}
