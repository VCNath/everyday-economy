import { Select } from "@/components/ui/Select";

export function LeaderboardFilters() {
  return (
    <div className="filter-row">
      <Select label="Geography" options={["Province", "CMA", "City"]} />
      <Select label="Period" options={["Latest", "1M", "3M", "12M"]} />
      <Select label="Sort" options={["Highest first", "Lowest first"]} />
      <Select label="Limit" options={["10", "25", "50"]} />
    </div>
  );
}
