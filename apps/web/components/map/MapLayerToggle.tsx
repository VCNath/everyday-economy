import { metricOptions } from "@/lib/constants";

export function MapLayerToggle() {
  return (
    <div className="map-layer-toggle" role="group" aria-label="Map metric layer">
      {metricOptions.slice(0, 6).map((metric) => (
        <button key={metric.id} className={metric.id === "cpi_food_yoy" ? "active" : ""} type="button">
          {metric.label}
        </button>
      ))}
    </div>
  );
}
