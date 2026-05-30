export function CompareInsightSummary({ insight }: { insight: string }) {
  return (
    <section className="panel summary-panel">
      <h2 className="section-title">Plain-English comparison</h2>
      <p>{insight}</p>
    </section>
  );
}
