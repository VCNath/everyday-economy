import { DatabaseZap } from "lucide-react";

export function DataFreshnessBadge({ period }: { period: string }) {
  return (
    <span className="badge" title="Latest source period">
      <DatabaseZap size={15} aria-hidden />
      Updated {period}
    </span>
  );
}
