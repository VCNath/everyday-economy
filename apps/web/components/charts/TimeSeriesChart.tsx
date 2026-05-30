import { Sparkline } from "./Sparkline";

export function TimeSeriesChart({
  title = "Food pressure over time",
  points = [2.1, 2.6, 3.2, 3.7, 3.5, 3.9, 3.7]
}: {
  title?: string;
  points?: number[];
}) {
  return (
    <section className="panel chart-panel">
      <p className="muted">Time series</p>
      <h2 className="section-title">{title}</h2>
      <Sparkline points={points.length ? points : [0]} />
    </section>
  );
}
