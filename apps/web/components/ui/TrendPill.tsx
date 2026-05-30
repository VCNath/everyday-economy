import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";

export function TrendPill({ value }: { value?: number | null }) {
  const trend = value ?? 0;
  const Icon = trend > 0 ? ArrowUpRight : trend < 0 ? ArrowDownRight : Minus;
  return (
    <span className={`trend-pill ${trend > 0 ? "up" : trend < 0 ? "down" : "flat"}`}>
      <Icon size={14} aria-hidden />
      {trend > 0 ? "+" : ""}
      {trend.toFixed(1)}%
    </span>
  );
}
