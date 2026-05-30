import { AppShell } from "@/components/layout/AppShell";
import { PageHero } from "@/components/ui/PageHero";
import { NpemCitationList } from "@/components/npem/NpemCitationList";
import { NpemProvenancePanel } from "@/components/npem/NpemProvenancePanel";
import { getNpemCitations, getNpemProvenance } from "@/lib/api-client";

export default async function NpemProvenancePage() {
  const [provenance, citations] = await Promise.all([getNpemProvenance({ province: "AB", group: "YA_UC" }), getNpemCitations({ province: "AB", group: "YA_UC" })]);
  return (
    <AppShell>
      <PageHero eyebrow="N.P.E.M. provenance" title="Sources, transformations, and citations" body="Every score should be traceable to a source or a clearly marked demo/proxy transformation." />
      <div className="two-col">
        <NpemProvenancePanel rows={provenance} />
        <NpemCitationList rows={citations} />
      </div>
    </AppShell>
  );
}
