import type { NpemScenario } from "@/lib/types";

export function NpemScenarioSelector({ scenarios, active }: { scenarios: NpemScenario[]; active: string }) {
  return (
    <div className="segmented-control" aria-label="N.P.E.M. scenario selector">
      {scenarios.map((scenario) => (
        <a key={scenario.scenario_code} className={scenario.scenario_code === active ? "active" : ""} href={`/npem?scenario=${scenario.scenario_code}`}>
          {scenario.label}
        </a>
      ))}
    </div>
  );
}
