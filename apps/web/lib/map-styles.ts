export const provinceFillColors = ["#d6eee5", "#a9d4c9", "#72a6a1", "#4d7583", "#334e68"];

export function getMapColor(value: number, min: number, max: number) {
  const span = Math.max(max - min, 1);
  const index = Math.min(provinceFillColors.length - 1, Math.floor(((value - min) / span) * provinceFillColors.length));
  return provinceFillColors[index];
}
