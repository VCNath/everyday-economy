export function CompareRegionSelector() {
  return (
    <div className="compare-selectors">
      <select aria-label="First region" defaultValue="Saskatchewan"><option>Saskatchewan</option><option>Alberta</option><option>Manitoba</option></select>
      <select aria-label="Second region" defaultValue="Alberta"><option>Saskatchewan</option><option>Alberta</option><option>Manitoba</option></select>
      <select aria-label="Third region" defaultValue="Manitoba"><option>Saskatchewan</option><option>Alberta</option><option>Manitoba</option></select>
    </div>
  );
}
