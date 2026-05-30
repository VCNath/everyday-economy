import { Skeleton } from "@mui/material";

export function LoadingSkeleton({ rows = 3 }: { rows?: number }) {
  return (
    <div className="loading-skeleton" aria-label="Loading">
      {Array.from({ length: rows }).map((_, index) => (
        <Skeleton key={index} variant="rounded" height={index === 0 ? 42 : 28} animation="wave" />
      ))}
    </div>
  );
}
