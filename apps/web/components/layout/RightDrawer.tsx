export function RightDrawer({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <aside className="right-drawer">
      <h2>{title}</h2>
      {children}
    </aside>
  );
}
