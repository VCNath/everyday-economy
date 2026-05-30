export function SidebarSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="sidebar-section">
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}
