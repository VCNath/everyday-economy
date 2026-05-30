import { LeaderboardPanel } from "@/components/leaderboard/LeaderboardPanel";
import type { LeaderboardRow } from "@/lib/types";

export function LeaderboardPreview({ rows }: { rows: LeaderboardRow[] }) {
  return <LeaderboardPanel rows={rows} />;
}
