"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { saveRegion, removeSavedRegion } from "@/lib/api-client";
import { useAuth } from "@/hooks/useAuth";

export function SaveRegionButton({ locationId }: { locationId: string }) {
  const auth = useAuth();
  const router = useRouter();
  const [saved, setSaved] = useState(false);
  const [pending, setPending] = useState(false);

  async function handleClick() {
    if (!auth.isAuthenticated || !auth.token) {
      router.push(`/auth/login?next=/regions/${locationId}`);
      return;
    }
    setPending(true);
    try {
      if (saved) {
        await removeSavedRegion(auth.token, locationId);
        setSaved(false);
      } else {
        await saveRegion(auth.token, { location_id: locationId });
        setSaved(true);
      }
    } finally {
      setPending(false);
    }
  }

  return (
    <button className={`button ${saved ? "secondary" : "primary"}`} type="button" onClick={handleClick} disabled={pending}>
      {pending ? "Saving..." : saved ? "Saved" : "Save Region"}
    </button>
  );
}
