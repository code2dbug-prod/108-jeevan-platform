import assert from "node:assert/strict";
import test from "node:test";

import { CARD_CATALOG, cardById, publicCards } from "./catalog";

test("catalog contains exactly 108 unique cards", () => {
  assert.equal(CARD_CATALOG.length, 108);
  assert.equal(new Set(CARD_CATALOG.map((card) => card.id)).size, 108);
});

test("Jeevan Number repeats 1 through 9 across the deck", () => {
  for (const card of CARD_CATALOG) {
    assert.equal(card.jeevanNumber, ((card.id - 1) % 9) + 1);
  }
});

test("public catalog excludes draft cards", () => {
  assert.ok(publicCards().every((card) => card.publicReady));
  assert.ok(publicCards().every((card) => card.id <= 27));
});

test("card lookup returns governed content", () => {
  const bharata = cardById(1);
  assert.equal(bharata.suit, "DHARMA");
  assert.equal(bharata.navaka, "SVADHARMA");
  assert.match(bharata.title, /Bharata/);
});
