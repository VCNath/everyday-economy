import { AuthButton } from "./topbar/AuthButton";
import { DataFreshnessBadge } from "./topbar/DataFreshnessBadge";
import { GlobalSearch } from "./topbar/GlobalSearch";
import { PeriodSelector } from "./topbar/PeriodSelector";
import { RegionSelector } from "./topbar/RegionSelector";
import { ThemeToggle } from "./topbar/ThemeToggle";

export function TopBar() {
  return (
    <header className="topbar">
      <GlobalSearch />
      <div className="topbar-actions">
        <RegionSelector />
        <PeriodSelector />
        <DataFreshnessBadge />
        <ThemeToggle />
        <AuthButton />
      </div>
    </header>
  );
}
