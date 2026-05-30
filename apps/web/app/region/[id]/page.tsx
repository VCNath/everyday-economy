import { redirect } from "next/navigation";

export default async function OldRegionRoute({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  redirect(`/regions/${id}`);
}
