import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";

export function RegionTrendCharts({ points }: { points?: number[] }) {
  return <TimeSeriesChart title="Regional trend" points={points} />;
}
