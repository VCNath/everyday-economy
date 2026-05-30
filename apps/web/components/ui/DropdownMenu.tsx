export function DropdownMenu({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="dropdown-scaffold">
      <button className="button" type="button">{label}</button>
      <div>{children}</div>
    </div>
  );
}
