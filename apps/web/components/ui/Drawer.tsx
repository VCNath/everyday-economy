export function Drawer({ title, children }: { title: string; children: React.ReactNode }) {
  return <aside className="drawer-scaffold"><h2>{title}</h2>{children}</aside>;
}
