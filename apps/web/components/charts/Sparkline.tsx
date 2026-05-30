export function Sparkline({ points }: { points: number[] }) {
  const max = Math.max(...points);
  const min = Math.min(...points);
  const coords = points
    .map((point, index) => {
      const x = (index / (points.length - 1)) * 120;
      const y = 36 - ((point - min) / Math.max(max - min, 1)) * 30;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg className="sparkline" viewBox="0 0 120 40" role="img" aria-label="Small trend line">
      <polyline points={coords} fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
