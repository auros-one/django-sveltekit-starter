.PHONY: help install dev test format lint clean setup-pre-commit sync-types reset-db fresh-start

help:
	@echo "Available commands:"
	@echo "  make install           - Install all dependencies"
	@echo "  make setup-pre-commit  - Install pre-commit hooks"
	@echo "  make sync-types        - Sync API types from backend to frontend"
	@echo "  make dev               - Start development environment"
	@echo "  make reset-db          - Reset database (WARNING: destroys all data)"
	@echo "  make fresh-start       - Reset database + setup dev environment"
	@echo "  make test              - Run all tests (auto-starts PostgreSQL)"
	@echo "  make format            - Format all code"
	@echo "  make lint              - Lint all code"
	@echo "  make clean             - Clean up generated files"

install:
	@echo "Installing backend dependencies..."
	cd backend && poetry install
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing pre-commit..."
	pip install pre-commit
	@echo "Setting up pre-commit hooks..."
	pre-commit install --install-hooks

setup-pre-commit:
	@echo "Installing pre-commit..."
	pip install pre-commit
	@echo "Setting up pre-commit hooks..."
	pre-commit install --install-hooks

sync-types:
	@echo "🔄 Generating OpenAPI schema from Django..."
	cd backend && poetry run python manage.py spectacular --file ../frontend/temp-schema.yml --validate --color
	@echo "🔄 Converting OpenAPI schema to TypeScript types..."
	cd frontend && npx openapi-typescript temp-schema.yml -o src/lib/api/schema.d.ts
	@echo "🎨 Formatting generated types..."
	cd frontend && npx prettier --write src/lib/api/schema.d.ts
	@echo "🧹 Cleaning up temporary files..."
	cd frontend && rm temp-schema.yml
	@echo "✅ API types synchronized successfully!"

dev:
	docker-compose up

dev-backend:
	cd backend && poetry run python manage.py runserver

dev-frontend:
	cd frontend && npm run dev

test:
	@echo "🔍 Checking if PostgreSQL is running..."
	@if ! docker compose ps db 2>/dev/null | grep -q "running"; then \
		echo "🚀 Starting PostgreSQL database..."; \
		docker compose up db -d; \
		echo "⏳ Waiting for database to be ready..."; \
		until docker compose exec db pg_isready -U postgres >/dev/null 2>&1; do \
			echo "Waiting for database to be ready..."; \
			sleep 2; \
		done; \
		echo "✅ Database is ready!"; \
	else \
		echo "✅ PostgreSQL is already running!"; \
	fi
	@echo "🧪 Running tests..."
	cd backend && DATABASE_URL=postgresql://postgres:postgres@localhost:5432/django_sveltekit_db poetry run pytest

format:
	cd backend && poetry run black .
	cd backend && poetry run isort .
	cd frontend && npm run format

lint:
	cd backend && poetry run ruff check .
	cd backend && poetry run pyright .
	cd frontend && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/.svelte-kit
	rm -rf frontend/build

reset-db:
	@echo "🚨 WARNING: This will destroy all database data!"
	@echo "Stopping and removing database container..."
	docker compose down db -v
	@echo "Waiting for database container to be removed..."
	@while docker compose ps db 2>/dev/null | grep -q db; do \
		echo "Waiting for db container to stop..."; \
		sleep 1; \
	done
	@echo "Starting fresh database container..."
	docker compose up db -d
	@echo "Waiting for database to be ready..."
	@until docker compose exec db pg_isready -U postgres >/dev/null 2>&1; do \
		echo "Waiting for database to be ready..."; \
		sleep 2; \
	done
	@echo "🔄 Running database migrations..."
	cd backend && DATABASE_URL=postgresql://postgres:postgres@localhost:5432/django_sveltekit_db poetry run python manage.py migrate
	@echo "✅ Database reset complete!"

fresh-start: reset-db
	@echo "🔄 Setting up development environment..."
	cd backend && DATABASE_URL=postgresql://postgres:postgres@localhost:5432/django_sveltekit_db poetry run python manage.py setup_dev_env
	@echo "✅ Fresh development environment ready!"
	@echo ""
	@echo "🎉 You can now login with:"
	@echo "   Email: admin@admin.com"
	@echo "   Password: admin"
