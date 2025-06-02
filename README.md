# Django-SvelteKit Starter

A production-ready monorepo template for building full-stack applications with Django and SvelteKit.

## Features
- **Django Backend**: REST API with Django REST Framework
- **SvelteKit Frontend**: Type-safe UI built with SvelteKit
- **Docker Compose**: One-command local development
- **GitHub Actions**: Automated CI/CD with path-based triggers

## Project Structure
```
django-sveltekit-starter/
├── backend/          # Django REST API
├── frontend/         # SvelteKit application
├── docker-compose.yml
├── Makefile
└── .github/
```

## Quick Start
```bash
make install  # install backend and frontend dependencies
make dev      # start local development stack
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

