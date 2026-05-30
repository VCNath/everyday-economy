export function formatMetric(value: number, unit: string) {
  if (unit === "CAD/month") return `$${Math.round(value).toLocaleString("en-CA")}/mo`;
  if (unit === "cents/litre") return `${value.toFixed(1)}c/L`;
  if (unit === "score") return `${Math.round(value)}/100`;
  if (unit === "%") return `${value.toFixed(1)}%`;
  return `${value.toLocaleString("en-CA")} ${unit}`;
}

export function signedPercent(value?: number) {
  if (value === undefined || value === null) return "n/a";
  return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
}
