export function ContentGrid({ children, columns = 2 }: { children: React.ReactNode; columns?: 2 | 3 }) {
  return <div className={`content-grid columns-${columns}`}>{children}</div>;
}
