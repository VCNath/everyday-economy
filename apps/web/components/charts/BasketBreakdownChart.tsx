const bars = [
  ["Protein", 34],
  ["Dairy", 20],
  ["Produce", 18],
  ["Bakery", 11],
  ["Other", 17]
];

export function BasketBreakdownChart() {
  return (
    <div className="bar-list">
      {bars.map(([label, value]) => (
        <div key={label}>
          <span>{label}</span>
          <i style={{ width: `${value}%` }} />
          <strong>{value}%</strong>
        </div>
      ))}
    </div>
  );
}
