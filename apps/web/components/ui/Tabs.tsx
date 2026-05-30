export function Tabs({ tabs, active }: { tabs: string[]; active: string }) {
  return (
    <div className="tabs">
      {tabs.map((tab) => (
        <button key={tab} className={tab === active ? "active" : ""} type="button">{tab}</button>
      ))}
    </div>
  );
}
