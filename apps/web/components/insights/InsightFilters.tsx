import { Select } from "@/components/ui/Select";

export function InsightFilters() {
  return (
    <div className="filter-row">
      <Select label="Type" options={["All", "Red flags", "Improvements", "Data releases"]} />
      <Select label="Region" options={["Canada", "Saskatchewan", "Ontario"]} />
    </div>
  );
}
