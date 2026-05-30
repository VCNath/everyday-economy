export function CachedBadge({ show }: { show: boolean }) {
  if (!show) return null;
  return <span className="badge neutral">Cached</span>;
}
