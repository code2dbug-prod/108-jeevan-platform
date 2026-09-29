# Professional Jyotisha calculation roadmap

The API calculates sidereal Grahas, Nakshatras, Pada and Lagna, supports
unknown-time uncertainty scanning, Vimshottari Mahadasha/Antardasha, current
Gochara snapshots, and full sign-based Parashari Graha Drishti.

## Implemented calculation policy

- Zodiac: sidereal
- Ayanamsha: Lahiri
- Bhava model: Whole Sign
- Full Graha Drishti:
  - all seven visible grahas: 7th
  - Mars: 4th, 7th, 8th
  - Jupiter: 5th, 7th, 9th
  - Saturn: 3rd, 7th, 10th
- Rahu/Ketu special aspects: intentionally **not assigned**. Node-aspect
  traditions vary and require an explicit, sourced project decision before use.
- Western square/trine/sextile/opposition aspect vocabulary is not used by the
  Jyotisha transit evidence engine.

## Source boundary

The full-drishṭi rule follows the classical Jyotisha pattern also stated in
Narada Purana 55.23 and standard Parashari teaching: all planets fully aspect
the seventh, Mars additionally the fourth/eighth, Jupiter fifth/ninth, and
Saturn third/tenth. This implementation currently records **full sign-based
drishti only**. Partial aspect-strength calculations are a separate research
module and are not inferred here.

## Remaining professional modules to implement and validate against golden charts

1. Rashi D1 Whole-Sign bhavas and bhava lords as explicit structured objects
2. D9 Navamsha and configurable Vargas
3. dignity: own sign, exaltation/debilitation, moolatrikona, combustion and retrogression
4. partial/quantified drishti strength, only after tradition/source policy is locked
5. Vimshottari Pratyantardasha and deeper levels
6. richer Gochara rule library beyond Graha Drishti
7. Ashtakavarga
8. curated yogas with explicit rule IDs
9. Sade Sati and major Saturn/Rahu/Ketu timing
10. Panchanga and current Moon/Nakshatra
11. compatibility and Guna Milan
12. Prashna and Varshaphala as separate modules

No interpretive text belongs inside calculation functions. Calculation outputs
must be structured facts with rule IDs and source/version metadata.
