.PHONY: help install dev test format lint clean setup-pre-commit sync-types

help:
	@echo "Available commands:"
	@echo "  make install           - Install all dependencies"
	@echo "  make setup-pre-commit  - Install pre-commit hooks"
	@echo "  make sync-types        - Sync API types from backend to frontend"
	@echo "  make dev               - Start development environment"
	@echo "  make test              - Run all tests"
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
	@echo "Syncing API types from backend to frontend..."
	cd frontend && npm run sync-types
	@echo "Types synced successfully!"

dev:
	docker-compose up

dev-backend:
	cd backend && poetry run python manage.py runserver

dev-frontend:
	cd frontend && npm run dev

test:
	@echo "Running backend tests..."
	cd backend && poetry run pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

format:
	cd backend && poetry run black .
	cd backend && poetry run isort .
	cd frontend && npm run format

lint:
	cd backend && poetry run flake8
	cd backend && poetry run mypy .
	cd frontend && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/.svelte-kit
	rm -rf frontend/build