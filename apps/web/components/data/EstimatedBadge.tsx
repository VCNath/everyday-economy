export function EstimatedBadge({ show }: { show: boolean }) {
  if (!show) return null;
  return <span className="badge warning">Estimated</span>;
}
