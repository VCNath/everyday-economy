export function Badge({ children, tone = "neutral" }: { children: React.ReactNode; tone?: "neutral" | "positive" | "warning" | "negative" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}
