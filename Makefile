.PHONY: help install dev test format lint clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Start development environment"
	@echo "  make test       - Run all tests"
	@echo "  make format     - Format all code"
	@echo "  make lint       - Lint all code"
	@echo "  make clean      - Clean up generated files"

install:
	@echo "Installing backend dependencies..."
	cd backend && poetry install
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

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
	cd backend && poetry run ruff check .
	cd backend && poetry run pyright .
	cd frontend && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/.svelte-kit
	rm -rf frontend/build
