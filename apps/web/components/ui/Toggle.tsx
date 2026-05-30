export function Toggle({ label }: { label: string }) {
  return <label className="toggle"><input type="checkbox" /> <span>{label}</span></label>;
}
