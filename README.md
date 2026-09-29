# 108-Jeevan Platform

Private professional Jyotisha + 108-Jeevan card reading platform.

This repository contains:
- `apps/web`: Next.js reader/customer application
- `apps/astrology-api`: FastAPI deterministic Jyotisha service
- `packages/contracts`: shared domain contracts
- `packages/jeevan-cards`: card-system data and interpretation primitives
- `supabase/migrations`: database schema and RLS foundations
- `docs`: architecture, calculation, security and development notes

> Important: deterministic astrology calculations and AI interpretation are intentionally separated. AI must never invent chart placements.

See `docs/architecture.md` for the full system boundary and `.env.example` for required configuration.
