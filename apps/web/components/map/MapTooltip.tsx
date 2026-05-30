import type { MapFeature } from "@/lib/types";

export function MapTooltip({ feature }: { feature: MapFeature }) {
  return (
    <div className="map-tooltip">
      <strong>{feature.name}</strong>
      <span>Food CPI: +{feature.value.toFixed(1)}% YoY</span>
      <span>Rank: {feature.rank}</span>
      <span>Updated: {feature.updated}</span>
    </div>
  );
}
