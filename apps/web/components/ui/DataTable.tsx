export function DataTable({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`data-table-shell ${className}`}>{children}</div>;
}
