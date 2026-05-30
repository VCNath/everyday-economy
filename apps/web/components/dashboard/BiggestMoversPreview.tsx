import { BiggestMovers } from "@/components/leaderboard/BiggestMovers";
import type { LeaderboardRow } from "@/lib/types";

export function BiggestMoversPreview({ rows }: { rows: LeaderboardRow[] }) {
  return <BiggestMovers rows={rows} />;
}
