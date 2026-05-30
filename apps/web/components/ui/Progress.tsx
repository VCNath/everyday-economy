export function Progress({ value }: { value: number }) {
  return <progress value={value} max={100}>{value}%</progress>;
}
