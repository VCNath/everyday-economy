import type { NpemGroup } from "@/lib/types";

export function NpemGroupSelector({ groups }: { groups: NpemGroup[] }) {
  return (
    <div className="filter-bar">
      {groups.slice(0, 8).map((group) => (
        <span key={group.group_code} className="status-pill neutral">
          {group.group_label}
        </span>
      ))}
    </div>
  );
}
