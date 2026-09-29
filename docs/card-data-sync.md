# Card data synchronization

The authoritative card-development workspace remains the 108-Jeevan Master Google Sheet and its linked Drive documents.

The application must not silently treat speculative astrology correspondences as canon.

## Application import target
A production card catalog record should include:
- card ID
- suit and Navaka
- title / Devanagari / transliteration
- mythic anchor
- Core / Prakasha / Chhaya / Marga
- keywords
- story role
- research/source status
- approval state
- provenance/version

The repo currently implements the immutable structural mapping (4 suits x 3 Navakas x 9 cards) and 1-9 Jeevan Number arithmetic. Canonical card text should be exported from the governed Sheet only after its status gate permits publication.

No Graha, Rashi, Bhava or Nakshatra assignment is considered canonical merely because a numerical mapping exists.
