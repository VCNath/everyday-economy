export function Input({ label, type = "text" }: { label: string; type?: string }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input type={type} />
    </label>
  );
}
