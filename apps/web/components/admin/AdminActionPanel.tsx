const actions: Array<{ label: string; endpoint: string }> = [
  { label: "Refresh All Sources", endpoint: "refresh-all" },
  { label: "Refresh CPI", endpoint: "refresh-cpi" },
  { label: "Refresh Gas", endpoint: "refresh-gas" },
  { label: "Refresh Labour", endpoint: "refresh-labour" },
  { label: "Build Leaderboards", endpoint: "build-leaderboards" },
  { label: "Calculate Baskets", endpoint: "calculate-baskets" },
  { label: "Evaluate Alerts", endpoint: "evaluate-alerts" },
  { label: "Generate Monthly Reports", endpoint: "generate-monthly-reports" },
];

export function AdminActionPanel({
  onRun,
  disabled = false,
}: {
  onRun?: (endpoint: string) => Promise<void> | void;
  disabled?: boolean;
}) {
  return (
    <section className="panel admin-actions">
      {actions.map((action) => (
        <button className="button" key={action.label} type="button" disabled={disabled} onClick={() => onRun?.(action.endpoint)}>
          {action.label}
        </button>
      ))}
    </section>
  );
}
