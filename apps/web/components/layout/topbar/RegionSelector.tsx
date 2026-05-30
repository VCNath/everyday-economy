import { MapPin } from "lucide-react";

export function RegionSelector() {
  return (
    <label className="topbar-select">
      <MapPin size={16} aria-hidden />
      <select aria-label="Region">
        <option>Canada</option>
        <option>Saskatchewan</option>
        <option>Saskatoon</option>
        <option>Ontario</option>
      </select>
    </label>
  );
}
