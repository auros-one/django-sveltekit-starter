# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Engineering Handbook

This project follows the engineering standards defined in our [Engineering Handbook](./docs/engineering-handbook/).
Key areas covered:
- Code standards for Python and TypeScript
- Development workflows and Git practices
- Architecture patterns and decisions
- Testing and security standards

**Always consult the handbook for best practices and standards.**

## Architecture Overview

This is a Django-SvelteKit monorepo with production-ready infrastructure:
- **Backend**: Django 4.2+ with DRF, JWT auth, Celery task queue
- **Frontend**: SvelteKit 2+ with TypeScript and type-safe API client
- **Infrastructure**: Docker Compose, PostgreSQL, Redis, S3 storage

## Key Development Commands

### Backend (Django)
```bash
cd backend/
poetry run python manage.py runserver  # Dev server
poetry run python manage.py migrate    # Run migrations
poetry run pytest                      # Run tests
docker compose up                      # Full stack
```

### Frontend (SvelteKit)
```bash
cd frontend/
npm run dev                    # Dev server (port 5173)
npm run sync-types            # Sync API types from backend (CRITICAL)
npm run build                 # Production build
npm run check                 # Type checking
```

## Critical Type Safety Pattern

The frontend uses **automatic OpenAPI type generation**:
1. Django generates OpenAPI schema at `/api/docs/schema`
2. Run `npm run sync-types` after any backend API changes
3. Frontend uses `openapi-fetch` with generated types for 100% type safety

**Always run `npm run sync-types` when modifying Django API endpoints.**

## Authentication Architecture

- **JWT tokens** stored in HTTP-only cookies (`refresh-token`)
- **Automatic token injection** via API client middleware
- **Route protection** in SvelteKit using server-side auth checks
- **Custom User model** uses email (not username) as primary identifier

## Important File Locations

- **Django settings**: `backend/project/settings.py`
- **API client**: `frontend/src/lib/api/index.ts`
- **Auth logic**: `frontend/src/routes/(auth)/+layout.server.ts`
- **User model**: `backend/project/accounts/models.py`

## Monorepo Structure

```
├── backend/     # Django API with Celery
├── frontend/    # SvelteKit app with Tailwind
└── MONOREPO-GUIDE.md    # Detailed setup instructions
```

## Development Workflow

1. **Adding API endpoints**: Create Django views/serializers
2. **Sync types**: Run `npm run sync-types`
3. **Frontend integration**: Use typed API client in components
4. **Testing**: `pytest` for backend, `npm run check` for frontend

The codebase emphasizes type safety between frontend/backend through automated OpenAPI schema generation.
