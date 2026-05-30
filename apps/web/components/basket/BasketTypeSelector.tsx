import { Select } from "@/components/ui/Select";

export function BasketTypeSelector() {
  return <Select label="Basket type" options={["Basic", "Student", "Family", "Commuter"]} />;
}
