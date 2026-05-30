export function InsightSourceLinks({ source, period }: { source: string; period: string }) {
  return <span className="source-badge">Sources: {source} · {period}</span>;
}
