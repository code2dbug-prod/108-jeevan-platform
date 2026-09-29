# 108-Jeevan Platform

Private professional Jyotisha + 108-Jeevan card reading platform.

## Architecture
- `apps/web` — Next.js reader + customer application
- `apps/astrology-api` — FastAPI deterministic Jyotisha engine
- `packages/contracts` — shared schemas
- `packages/jeevan-cards` — governed 108-card catalog, deck structure, spreads and 1–9 memory system
- `packages/interpretation` — evidence packet + AI synthesis guardrails
- `supabase/migrations` — auth/profile/readings/report/privacy database + RLS
- `docs` — architecture, calculation and operations notes

## Core rule
AI never calculates planets, houses, Vargas, Dashas, transits or card IDs. Deterministic services generate evidence; AI may only synthesize supplied evidence.

## Local development
1. Copy `.env.example` to `.env.local` and add Supabase/OpenAI keys as needed.
2. Run the astrology API from `apps/astrology-api`.
3. Run `pnpm install` then `pnpm dev` from the repo root.
4. Apply Supabase migrations in order before using authenticated persistence.

See:
- `docs/architecture.md`
- `docs/local-development.md`
- `docs/product-completion-status.md`
- `docs/card-catalog-governance.md`
