import Link from "next/link";

export function BetaBanner() {
  return (
    <div className="beta-banner" role="status">
      <strong>Public beta:</strong>
      <span>Data coverage, scoring, and alerts are still being refined.</span>
      <Link href="/help/known-limitations">Known limitations</Link>
      <Link href="/data/methodology">Methodology</Link>
    </div>
  );
}
