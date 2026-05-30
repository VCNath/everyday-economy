import { FreshnessBadge } from "@/components/data/FreshnessBadge";
import type { CompareMetricRow } from "@/lib/types";

export function CompareMetricTable({
  rows,
  locationNames
}: {
  rows: CompareMetricRow[];
  locationNames: string[];
}) {
  const grouped = rows.reduce<Record<string, CompareMetricRow[]>>((acc, row) => {
    const key = `${row.indicator_id}::${row.indicator_name}::${row.unit}`;
    acc[key] = acc[key] ? [...acc[key], row] : [row];
    return acc;
  }, {});

  return (
    <section className="panel">
      <table className="compact-table">
        <thead><tr><th>Metric</th>{locationNames.map((name) => <th key={name}>{name}</th>)}</tr></thead>
        <tbody>
          {Object.entries(grouped).map(([key, metricRows]) => {
            const [indicatorId, indicatorName, unit] = key.split("::");
            return (
            <tr key={indicatorId}>
              <td>{indicatorName}</td>
              {locationNames.map((locationName) => {
                const row = metricRows.find((item) => item.location_name === locationName);
                return (
                <td key={`${indicatorId}-${locationName}`}>
                  {row && row.value !== null ? `${row.value.toFixed(1)} ${unit}` : "—"}
                  {row ? <FreshnessBadge status={row.trust.freshness_status} /> : null}
                </td>
              );})}
            </tr>
          );})}
        </tbody>
      </table>
    </section>
  );
}
