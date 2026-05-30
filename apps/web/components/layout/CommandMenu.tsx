import { Search } from "lucide-react";

export function CommandMenu() {
  return (
    <div className="command-menu-scaffold" aria-hidden>
      <Search size={16} />
      <span>Command search scaffold: regions, indicators, pages, and sources.</span>
    </div>
  );
}
