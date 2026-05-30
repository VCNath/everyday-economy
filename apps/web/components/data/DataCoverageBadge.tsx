export function DataCoverageBadge({ coverageScore }: { coverageScore?: number | null }) {
  if (coverageScore === undefined || coverageScore === null) return null;
  return <span className="badge neutral">Coverage {(coverageScore * 100).toFixed(0)}%</span>;
}
