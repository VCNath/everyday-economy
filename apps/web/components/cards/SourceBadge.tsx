export function SourceBadge({ source, period }: { source: string; period: string }) {
  return (
    <span className="source-badge">
      Source: {source} · {period}
    </span>
  );
}
