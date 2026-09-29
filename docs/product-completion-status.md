# Product completion status

## Implemented
- Next.js reader/customer application foundation.
- Supabase auth-ready profiles, birth profiles, chart snapshots, readings, draws, evidence, notes, reports and privacy requests.
- Deterministic Python/FastAPI Jyotisha service using Lahiri sidereal mode.
- Graha positions, Nakshatra/Pada, whole-sign houses, sign lordship, basic dignity, D9/Navamsa projection and Panchanga indices.
- Vimshottari Mahadasha, Antardasha and Pratyantardasha.
- Parashari full-sign Graha Drishti for the seven visible grahas. Node drishti deliberately remains unassigned until a source tradition is locked.
- Unknown-birth-time 24-hour uncertainty sweep.
- Governed 108-card catalog synced from the project Sheet.
- 1-9 Jeevan-number memory helpers.
- Spread drawing and evidence-packet synthesis.
- Optional OpenAI synthesis endpoint that receives evidence only; it is forbidden from calculating or inventing placements.
- CI for TypeScript/Next.js and Python.

## Intentionally not hard-coded
- Permanent Graha/Rashi/Bhava/Nakshatra assignments for the 108 cards.
- Rahu/Ketu special drishti.
- A single traditional interpretation for disputed Jyotisha schools.
- Birth-time rectification claims.

These remain research/governance decisions, not missing code.

## Production dependencies still requiring account configuration
- Supabase project and keys.
- OPENAI_API_KEY if AI narrative synthesis is desired.
- Swiss Ephemeris production licensing decision.
- Deployment targets (Vercel for web; Railway/AWS/container host for astrology API).
