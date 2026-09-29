# System architecture

## Boundary
The platform has three trust zones:
1. **Web application** — reader console and customer portal.
2. **Deterministic Jyotisha engine** — astronomical and rule-based calculations only.
3. **Interpretation layer** — combines verified astrology facts, 108-Jeevan card canon, spread semantics and reader notes. It may use an LLM but cannot invent calculations.

## Request flow
Birth profile -> deterministic chart snapshot -> current timing snapshot -> question classification -> card draw -> evidence graph -> synthesis -> reader review -> customer publication.

## Canonical calculation settings
- Zodiac: sidereal
- Ayanamsha: Lahiri
- Houses: whole sign
- Nodes: mean node initially, configurable later
- Timezone: IANA zone stored with calculation metadata

## Unknown birth time
Never substitute noon as if exact. Run an uncertainty sweep across the local civil day. Stable factors may be shown; Lagna, houses and Vargas are suppressed unless explicitly stable. Birth-time rectification is a separate future workflow.

## Security
All customer birth data is protected by Supabase RLS. Reader-only tables include private notes and audit history. Published reports should contain only explicitly selected fields.
