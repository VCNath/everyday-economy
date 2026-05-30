import { EconomicMap } from "@/components/map/EconomicMap";
import type { MapFeature } from "@/lib/types";

export function DashboardMapPreview({ features }: { features: MapFeature[] }) {
  return <EconomicMap features={features} />;
}
