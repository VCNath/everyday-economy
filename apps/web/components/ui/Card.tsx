export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`panel card ${className}`}>{children}</section>;
}
