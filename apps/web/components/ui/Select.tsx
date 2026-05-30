export function Select({
  label,
  options,
  value,
  onChange
}: {
  label: string;
  options: string[];
  value?: string;
  onChange?: (value: string) => void;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={onChange ? (event) => onChange(event.target.value) : undefined}>
        {options.map((option) => <option key={option}>{option}</option>)}
      </select>
    </label>
  );
}
