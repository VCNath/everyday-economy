import type { MapFeature } from "@/lib/types";

export function RegionClickPanel({ feature }: { feature: MapFeature }) {
  return (
    <aside className="region-click-panel">
      <p className="muted">Map selection</p>
      <strong>{feature.name}</strong>
      <span>Food price pressure is +{feature.value.toFixed(1)}% year-over-year.</span>
      <span>Ranked {feature.rank} for the active layer.</span>
    </aside>
  );
}
