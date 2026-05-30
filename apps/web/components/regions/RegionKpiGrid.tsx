import { RegionSummaryCard } from "@/components/cards/RegionSummaryCard";
import type { RegionSummary } from "@/lib/types";

export function RegionKpiGrid({ summary }: { summary: RegionSummary }) {
  return <RegionSummaryCard summary={summary} />;
}
