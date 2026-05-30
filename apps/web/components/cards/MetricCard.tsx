import { ArrowDownRight, ArrowUpRight } from "lucide-react";

import { signedPercent } from "@/lib/formatters";

interface MetricCardProps {
  label: string;
  value: string;
  helper: string;
  trend?: number;
  tone?: "positive" | "negative" | "warning" | "neutral";
}

export function MetricCard({ label, value, helper, trend, tone = "neutral" }: MetricCardProps) {
  const TrendIcon = (trend ?? 0) > 0 ? ArrowUpRight : ArrowDownRight;
  return (
    <article className={`metric-card ${tone}`}>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
      </div>
      {trend !== undefined ? (
        <span className="metric-trend">
          <TrendIcon size={15} aria-hidden />
          {signedPercent(trend)}
        </span>
      ) : null}
      <small>{helper}</small>
    </article>
  );
}
