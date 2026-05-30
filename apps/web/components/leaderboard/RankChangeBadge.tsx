import { ArrowDown, ArrowRight, ArrowUp } from "lucide-react";

export function RankChangeBadge({ change = 0 }: { change?: number | null }) {
  const normalizedChange = change ?? 0;
  const Icon = normalizedChange > 0 ? ArrowUp : normalizedChange < 0 ? ArrowDown : ArrowRight;
  return (
    <span className={`rank-change ${normalizedChange > 0 ? "up" : normalizedChange < 0 ? "down" : "flat"}`}>
      <Icon size={14} aria-hidden />
      {normalizedChange === 0 ? "No change" : Math.abs(normalizedChange)}
    </span>
  );
}
