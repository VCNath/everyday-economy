import { EstimatedBadge } from "@/components/data/EstimatedBadge";

export function BasketItemTable() {
  return (
    <section className="panel">
      <table className="compact-table">
        <thead><tr><th>Item</th><th>Quantity</th><th>Unit price</th><th>Monthly cost</th></tr></thead>
        <tbody>
          <tr><td>Milk, 2L</td><td>4</td><td>$5.08</td><td>$20.32</td></tr>
          <tr><td>Eggs, dozen</td><td>2</td><td>$4.60</td><td>$9.20</td></tr>
          <tr><td>Bread</td><td>6</td><td>$3.35</td><td>$20.10</td></tr>
          <tr><td>Rent placeholder <EstimatedBadge show={true} /></td><td>1</td><td>$1,200</td><td>$1,200</td></tr>
        </tbody>
      </table>
    </section>
  );
}
