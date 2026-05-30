import { provinceFillColors } from "@/lib/map-styles";

export function MapLegend({ label }: { label: string }) {
  return (
    <div className="map-legend" aria-label={`${label} legend`}>
      <span>Low</span>
      <div className="legend-scale">
        {provinceFillColors.map((color) => (
          <i key={color} style={{ background: color }} />
        ))}
      </div>
      <span>High</span>
    </div>
  );
}
