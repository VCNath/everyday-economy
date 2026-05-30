export function Dialog({ title, children }: { title: string; children: React.ReactNode }) {
  return <div className="dialog-scaffold"><strong>{title}</strong>{children}</div>;
}
