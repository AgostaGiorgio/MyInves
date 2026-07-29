# AGENTS.md — myInves

## Repo structure

Monorepo with two independent packages: `backend/` (Python/FastAPI) and `frontend/` (Vue 3/Vite). No monorepo tooling, no workspaces. No tests, no CI/CD workflows, no docker-compose.

## Backend

- **Deps:** Poetry with `poetry.toml` setting `create = false` (virtualenvs disabled — installs into system Python).
- **Start (dev):** `poetry run python src/main.py` (not uvicorn directly).
- **Start (Docker):** `poetry run uvicorn src.main:app --port 8080 --host 0.0.0.0`
- **Migrations:** `yoyo apply --database <db_url> ./migrations` (SQL files in `backend/migrations/`).
- **Config:** `pydantic-settings` reads from `backend/.env` — PostgreSQL creds + optional `ORBIT_API_URL`.
- **DB:** Async SQLAlchemy + asyncpg, raw SQL via `text()` in `src/services/queries.py` (no ORM query building).
- **DI:** `dependency-injector` wires `PortfolioService` into routers (`src/di.py`).
- **CORS:** Permissive (all origins).
- No linter/formatter config exists.

## Frontend

- **Start:** `npm run dev` (Vite dev server).
- **Build:** `npm run build` → static to `dist/`, served via nginx in Docker.
- **API URL:** `VITE_API_BASE_URL` env var (default `http://localhost:8000`).
- **Docker build arg:** `VITE_API_BASE_URL` needed at build time for the nginx stage.
- **Styling:** Tailwind CSS with custom Orbit Ecosystem dark theme preset (`orbit-ecosystem-preset.js`).
- **State:** No router, no state library — single-page app with `ref`/`onMounted` in `App.vue`.
- No linter/formatter config exists.

## Docker

```sh
# Backend (linux/amd64)
docker buildx build --platform linux/amd64 -t registry/myinves_be:x.y.z backend/

# Frontend (linux/amd64)
docker buildx build --platform linux/amd64 \
  --build-arg VITE_API_BASE_URL=https://backend:8000 \
  -t registry/myinves_fe:x.y.z frontend/
```

Deployed externally via ArgoCD.

## Quirks & conventions

- `poetry.toml` is tracked in git despite `.gitignore` listing it.
- `BANK_ACCOUNT_STATIC` in `AssetTypeEnum` but absent from DB migrations.
- API POST `/assets` accepts raw `Asset` with optional `id` (UUID is DB-generated).
- Orbit client pings `ORBIT_API_URL` every hour on a daemon thread; disabled when URL is empty.
- yoyo.ini contains hardcoded DB credentials (local dev only).
- No test framework or any test files exist anywhere.
