export function FreshnessBadge({ status }: { status?: string | null }) {
  const normalized = (status ?? "unavailable").toLowerCase();
  const label = normalized.charAt(0).toUpperCase() + normalized.slice(1);
  const tone =
    normalized === "healthy"
      ? "positive"
      : normalized === "stale" || normalized === "error"
        ? "negative"
        : normalized === "partial" || normalized === "estimated" || normalized === "cached"
          ? "warning"
          : "neutral";
  return <span className={`badge ${tone}`}>{label}</span>;
}
