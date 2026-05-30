import type { NpemProvenance } from "@/lib/types";

export function NpemProvenancePanel({ rows }: { rows: NpemProvenance[] }) {
  return (
    <section className="panel">
      <h3>Provenance</h3>
      {rows.length ? rows.map((row) => (
        <p key={row.provenance_id}>{row.source_system}: {row.transform_step} · {row.licence_note}</p>
      )) : <p>No provenance records returned yet.</p>}
    </section>
  );
}
