export function ErrorState() {
  return (
    <div className="error-state">
      <h2>We could not refresh CPI data right now.</h2>
      <p>Showing the latest cached data from April 2026.</p>
      <button className="button" type="button">Retry</button>
    </div>
  );
}
