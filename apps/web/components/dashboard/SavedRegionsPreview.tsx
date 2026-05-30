import { EmptyState } from "@/components/ui/EmptyState";

export function SavedRegionsPreview() {
  return (
    <section className="panel saved-preview">
      <EmptyState
        title="No saved regions yet"
        body="Save provinces or cities to build your personal economic watchlist."
        action="Explore Map"
        href="/map"
      />
    </section>
  );
}
