# Local development

## Requirements
- Node.js 22+
- Corepack + pnpm
- Python 3.12+
- Docker Desktop (recommended)
- Supabase CLI for local DB/auth

## Start web workspace
```bash
corepack enable
pnpm install
pnpm dev
```

## Start astrology API
```bash
cd apps/astrology-api
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

## Docker
```bash
docker compose up --build
```

Copy `.env.example` to local environment files. Never commit service-role keys.
