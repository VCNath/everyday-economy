const tabs = ["Overall", "Groceries", "Housing", "Gas", "Jobs"];

export function LeaderboardTabs() {
  return (
    <div className="tabs" role="tablist" aria-label="Leaderboard groups">
      {tabs.map((tab) => (
        <button key={tab} className={tab === "Groceries" ? "active" : ""} type="button">
          {tab}
        </button>
      ))}
    </div>
  );
}
