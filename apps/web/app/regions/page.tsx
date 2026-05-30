import Link from "next/link";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/layout/PageHeader";
import { getLocations } from "@/lib/api-client";

export default async function RegionsPage() {
  const locations = await getLocations();
  const regions = locations
    .filter((location) => location.id !== "CA" && (location.geography_level === "province" || location.geography_level === "territory"))
    .sort((a, b) => a.name.localeCompare(b.name));
  return (
    <AppShell>
      <PageHeader title="Region Profiles" subtitle="Browse provinces, territories, and later city-level profiles." />
      <section className="region-grid">
        {regions.map((region) => {
          return <Link className="panel region-link" href={`/regions/${region.id}`} key={region.id}>{region.name}<span>{region.id}</span></Link>;
        })}
      </section>
    </AppShell>
  );
}
