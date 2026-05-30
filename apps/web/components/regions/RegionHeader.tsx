import { PageHeader } from "@/components/layout/PageHeader";
import { Button } from "@/components/ui/Button";
import { SaveRegionButton } from "@/components/regions/SaveRegionButton";
import Link from "next/link";

export function RegionHeader({ name, locationId }: { name: string; locationId: string }) {
  return (
    <PageHeader
      title={name}
      subtitle="Regional economic profile and household pressure signals."
      primaryAction={<SaveRegionButton locationId={locationId} />}
      secondaryAction={
        <div className="row">
          <Button href="/compare">Compare</Button>
          <Link className="button" href={`/account/alerts?location=${locationId}`}>Create alert</Link>
          <Link className="button" href="/account/reports">Generate report</Link>
        </div>
      }
    />
  );
}
