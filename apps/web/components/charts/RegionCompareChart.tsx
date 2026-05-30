const regions = [
  ["Saskatchewan", 72],
  ["Manitoba", 76],
  ["Ontario", 56]
];

export function RegionCompareChart() {
  return (
    <section className="panel compare-chart">
      <p className="muted">Region comparison</p>
      <h2 className="section-title">Affordability score</h2>
      <div className="bar-list">
        {regions.map(([label, value]) => (
          <div key={label}>
            <span>{label}</span>
            <i style={{ width: `${value}%` }} />
            <strong>{value}/100</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
