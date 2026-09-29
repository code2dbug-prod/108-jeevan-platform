# Interpretation engine

The interpretation layer operates on an **evidence graph**, not raw prose prompts.

Evidence classes:
- natal
- Dasha
- transit
- card
- card combination
- reader note
- source/provenance

Pipeline:
1. classify the user's question into one or more life domains;
2. select relevant natal facts;
3. attach active Mahadasha/Antardasha and current transit events;
4. attach drawn card meanings, spread positions and combinations;
5. build a structured synthesis packet with confidence;
6. only then pass the packet to an LLM for natural-language synthesis;
7. reader reviews/edits before publication.

The LLM must not create planets, degrees, houses, Dashas, yogas, source quotations, or card canon not present in evidence.
