import { Lightbulb } from "lucide-react";

export function InsightCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="panel insight-card">
      <div className="insight-title">
        <Lightbulb size={18} aria-hidden />
        <h2 className="section-title">{title}</h2>
      </div>
      <p>{children}</p>
    </section>
  );
}
