export const JEEVAN_NUMBER_HOOKS = {
  1: { key: "seed", prompt: "What begins, leads, or stands alone?" },
  2: { key: "mirror", prompt: "What relates, reflects, or divides?" },
  3: { key: "triangle", prompt: "What grows through a third factor?" },
  4: { key: "foundation", prompt: "What needs structure, boundary, or stability?" },
  5: { key: "crossroads", prompt: "What changes, moves, or must be chosen?" },
  6: { key: "bond", prompt: "What must be cared for, harmonized, or carried?" },
  7: { key: "lamp", prompt: "What asks for inward search, faith, or testing?" },
  8: { key: "wheel", prompt: "What concerns power, consequence, or endurance?" },
  9: { key: "completion", prompt: "What completes, releases, or returns to the whole?" },
} as const;

export function jeevanNumber(cardId: number): 1|2|3|4|5|6|7|8|9 {
  if (!Number.isInteger(cardId) || cardId < 1 || cardId > 108) throw new RangeError("cardId must be 1..108");
  return (((cardId - 1) % 9) + 1) as 1|2|3|4|5|6|7|8|9;
}

export function cardsForJeevanNumber(value: number): number[] {
  if (!Number.isInteger(value) || value < 1 || value > 9) throw new RangeError("value must be 1..9");
  return Array.from({ length: 12 }, (_, i) => value + i * 9);
}
