import { Search } from "lucide-react";

export function GlobalSearch() {
  return (
    <button className="topbar-search" type="button" aria-label="Open command search">
      <Search size={17} aria-hidden />
      <span>Search regions, indicators, sources...</span>
      <kbd>⌘K</kbd>
    </button>
  );
}
