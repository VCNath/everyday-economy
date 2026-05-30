import type { NpemCitation } from "@/lib/types";

export function NpemCitationList({ rows }: { rows: NpemCitation[] }) {
  return (
    <section className="panel">
      <h3>Citations</h3>
      <ul className="clean-list">
        {rows.map((row, index) => <li key={`${row.source_system}-${index}`}>{row.citation_text ?? row.source_system}</li>)}
      </ul>
    </section>
  );
}
