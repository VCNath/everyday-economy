export function PageTabs({ tabs, active }: { tabs: string[]; active: string }) {
  return (
    <div className="page-tabs" role="tablist">
      {tabs.map((tab) => (
        <button key={tab} className={tab === active ? "active" : ""} type="button">
          {tab}
        </button>
      ))}
    </div>
  );
}
