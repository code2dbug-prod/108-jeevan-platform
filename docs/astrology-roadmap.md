# Professional Jyotisha calculation roadmap

The API skeleton already calculates sidereal Grahas, Nakshatras, Pada and Lagna and supports unknown-time uncertainty scanning.

Production modules to implement and validate against golden charts:
1. Rashi D1 + whole-sign bhavas and lords
2. D9 Navamsha and configurable Vargas
3. dignity: own sign, exaltation/debilitation, moolatrikona, combustion and retrogression
4. Parashari drishti
5. Vimshottari Mahadasha / Antardasha / Pratyantardasha
6. Gochara and transit-to-natal hits
7. Ashtakavarga
8. curated yogas with explicit rule IDs
9. Sade Sati and major Saturn/Rahu/Ketu timing
10. Panchanga and current Moon/Nakshatra
11. compatibility and Guna Milan
12. Prashna and Varshaphala as separate modules

No interpretive text belongs inside calculation functions. Calculation outputs must be structured facts with rule IDs and source/version metadata.
