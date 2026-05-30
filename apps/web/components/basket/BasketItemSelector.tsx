const items = ["Milk", "Eggs", "Bread", "Chicken", "Apples"];

export function BasketItemSelector() {
  return (
    <div className="basket-items">
      {items.map((item, index) => (
        <label key={item}>
          <span>{item}</span>
          <input type="number" min="0" defaultValue={index < 3 ? 2 : 1} aria-label={`${item} quantity`} />
        </label>
      ))}
    </div>
  );
}
