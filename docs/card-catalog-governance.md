# Card catalog governance

The application card catalog is a **snapshot** of the governed Google Sheet, not a second source of truth.

Source:
- Spreadsheet: `108-JEEVAN_MASTER-CARD-MATRIX`
- Tab: `01_CARD_REGISTRY`
- Current imported range: `A1:V109`

Rules:
1. The Sheet remains authoritative.
2. A GitHub snapshot must preserve the Sheet's current statuses.
3. `publicReady` is a derived runtime gate; it does not promote a card.
4. DRAFT, RESEARCHED and REVIEWED cards may be visible in the private Reader Console but must not be exposed as finalized client canon.
5. No Graha/Rashi/Bhava/Nakshatra correspondence is inferred by the sync.
6. A LOCKED card cannot be silently changed in code; update the governed source first and regenerate the snapshot.

The current snapshot contains 108 records. At generation time, 27 cards qualify for the public-ready gate and 81 remain internal-development records.
