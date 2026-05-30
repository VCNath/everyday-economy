import { CachedBadge } from "./CachedBadge";
import { DataCoverageBadge } from "./DataCoverageBadge";
import { EstimatedBadge } from "./EstimatedBadge";
import { FreshnessBadge } from "./FreshnessBadge";

export function TrustBadge({
  freshnessStatus,
  isEstimated,
  isCached,
  coverageScore
}: {
  freshnessStatus?: string | null;
  isEstimated?: boolean;
  isCached?: boolean;
  coverageScore?: number | null;
}) {
  return (
    <span className="trust-badges">
      <FreshnessBadge status={freshnessStatus} />
      <EstimatedBadge show={Boolean(isEstimated)} />
      <CachedBadge show={Boolean(isCached)} />
      <DataCoverageBadge coverageScore={coverageScore} />
    </span>
  );
}
