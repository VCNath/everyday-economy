"use client";

import { useMemo, useState } from "react";
import { LocateFixed } from "lucide-react";

import { getMapColor } from "@/lib/map-styles";
import type { MapFeature } from "@/lib/types";
import { MapLayerToggle } from "./MapLayerToggle";
import { MapLegend } from "./MapLegend";
import { MapTooltip } from "./MapTooltip";
import { RegionClickPanel } from "./RegionClickPanel";

const tilePositions: Record<string, { gridColumn: string; gridRow: string }> = {
  "CA-YT": { gridColumn: "2 / span 2", gridRow: "1 / span 2" },
  "CA-NT": { gridColumn: "4 / span 2", gridRow: "1 / span 2" },
  "CA-NU": { gridColumn: "6 / span 3", gridRow: "1 / span 2" },
  "CA-BC": { gridColumn: "2 / span 2", gridRow: "3 / span 2" },
  "CA-AB": { gridColumn: "4 / span 1", gridRow: "3 / span 2" },
  "CA-SK": { gridColumn: "5 / span 1", gridRow: "3 / span 2" },
  "CA-MB": { gridColumn: "6 / span 1", gridRow: "3 / span 2" },
  "CA-ON": { gridColumn: "7 / span 2", gridRow: "4 / span 2" },
  "CA-QC": { gridColumn: "9 / span 2", gridRow: "3 / span 2" },
  "CA-NB": { gridColumn: "10 / span 1", gridRow: "5 / span 1" },
  "CA-NS": { gridColumn: "11 / span 1", gridRow: "5 / span 1" },
  "CA-PE": { gridColumn: "11 / span 1", gridRow: "4 / span 1" },
  "CA-NL": { gridColumn: "12 / span 2", gridRow: "3 / span 2" }
};

export function EconomicMap({ features }: { features: MapFeature[] }) {
  const [selectedId, setSelectedId] = useState("CA-SK");
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const values = features.map((feature) => feature.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const selected = features.find((feature) => feature.location_id === selectedId) ?? features[0];
  const hovered = useMemo(
    () => features.find((feature) => feature.location_id === hoveredId),
    [features, hoveredId]
  );

  return (
    <section className="panel map-panel">
      <div className="map-panel-header">
        <div>
          <p className="muted">Canada map</p>
          <h1>Where household pressure is moving</h1>
        </div>
        <button className="button" type="button" title="Fit Canada view">
          <LocateFixed size={17} aria-hidden />
          Fit
        </button>
      </div>
      <MapLayerToggle />
      <div className="tile-map" role="img" aria-label="Tile map of Canadian provinces and territories by food CPI">
        {features.map((feature) => (
          <button
            key={feature.location_id}
            className={`province-tile ${feature.location_id === selectedId ? "selected" : ""}`}
            style={{
              ...tilePositions[feature.location_id],
              background: getMapColor(feature.value, min, max)
            }}
            type="button"
            onClick={() => setSelectedId(feature.location_id)}
            onMouseEnter={() => setHoveredId(feature.location_id)}
            onMouseLeave={() => setHoveredId(null)}
            aria-label={`${feature.name}: ${feature.value.toFixed(1)} percent year over year`}
          >
            {feature.location_id.replace("CA-", "")}
          </button>
        ))}
        {hovered ? <MapTooltip feature={hovered} /> : null}
      </div>
      <div className="map-bottom">
        <MapLegend label="Food CPI YoY" />
        <RegionClickPanel feature={selected} />
      </div>
    </section>
  );
}
