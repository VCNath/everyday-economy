import { redirect } from "next/navigation";

export default function OldApiStatusRoute() {
  redirect("/data/api-status");
}
