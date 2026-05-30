export function PageHeader({
  title,
  subtitle,
  primaryAction,
  secondaryAction,
  metadata
}: {
  title: string;
  subtitle: string;
  primaryAction?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  metadata?: React.ReactNode;
}) {
  return (
    <div className="page-header">
      <div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
        {metadata ? <div className="page-metadata">{metadata}</div> : null}
      </div>
      {(primaryAction || secondaryAction) && (
        <div className="page-actions">
          {secondaryAction}
          {primaryAction}
        </div>
      )}
    </div>
  );
}
