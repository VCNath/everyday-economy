import { CalendarDays } from "lucide-react";

export function PeriodSelector() {
  return (
    <label className="topbar-select">
      <CalendarDays size={16} aria-hidden />
      <select aria-label="Period">
        <option>Latest</option>
        <option>Previous month</option>
        <option>Previous year</option>
        <option>Custom</option>
      </select>
    </label>
  );
}
