import { Button } from "./Button";

export function EmptyState({ title, body, action, href }: { title: string; body: string; action?: string; href?: string }) {
  return (
    <div className="empty-state">
      <h2>{title}</h2>
      <p>{body}</p>
      {action && href ? <Button href={href} variant="primary">{action}</Button> : null}
    </div>
  );
}
