export function Skeleton({ rows = 1 }: { rows?: number }) {
  return <div className="skeleton-stack">{Array.from({ length: rows }).map((_, index) => <i key={index} />)}</div>;
}
