import rawCatalog from "../data/cards.generated.json";

export type CatalogCard = (typeof rawCatalog.cards)[number];

export const CARD_CATALOG: readonly CatalogCard[] = rawCatalog.cards;
export const CARD_CATALOG_META = rawCatalog.generatedFrom;

export function cardById(cardId: number): CatalogCard {
  const card = CARD_CATALOG.find((item) => item.id === cardId);
  if (!card) throw new RangeError(`Unknown card ID: ${cardId}`);
  return card;
}

export function publicCards(): readonly CatalogCard[] {
  return CARD_CATALOG.filter((card) => card.publicReady);
}

export function cardsByNavaka(navaka: string): readonly CatalogCard[] {
  return CARD_CATALOG.filter((card) => card.navaka === navaka);
}
