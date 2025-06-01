# Django-SvelteKit Starter

A production-ready monorepo template for building full-stack applications with Django (backend) and SvelteKit (frontend).

## 🚀 Features

- **Django Backend**: REST API with Django REST Framework
- **SvelteKit Frontend**: Type-safe, fast, and modern UI
- **Docker Compose**: One-command local development
- **GitHub Actions**: Automated CI/CD with path-based triggers
- **Type Safety**: Auto-generated TypeScript types from Django
- **Monorepo Benefits**: Atomic commits, shared tooling, simplified workflow

## 📦 Project Structure

```
django-sveltekit-starter/
├── backend/          # Django REST API
├── frontend/         # SvelteKit application  
├── docker-compose.yml
├── Makefile         # Common development commands
└── .github/         # CI/CD workflows
```

## 🛠️ Prerequisites

- Python 3.11+
- Node.js 22+
- Docker & Docker Compose
- Poetry (Python package manager)

## 🏃 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/auros-one/django-sveltekit-starter.git
   cd django-sveltekit-starter
   ```

2. **Install dependencies**
   ```bash
   make install
   ```

3. **Start development environment**
   ```bash
   make dev
   ```

4. **Access the applications**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin

## 📝 Development Commands

```bash
make help        # Show all available commands
make install     # Install all dependencies
make dev         # Start Docker Compose stack
make test        # Run all tests
make format      # Format code
make lint        # Lint code
make clean       # Clean generated files
```

## 🔧 Configuration

### Backend
- Configuration: `backend/.env`
- Database: PostgreSQL (via Docker)
- API Docs: http://localhost:8000/api/schema/swagger-ui/

### Frontend  
- Configuration: `frontend/.env`
- API URL: Set via `PUBLIC_API_URL` environment variable

## 🚢 Deployment

Both frontend and backend can be deployed independently:

- **Backend**: Deploy as a standard Django application
- **Frontend**: Deploy to any static hosting service

## 📄 License

MIT License - see LICENSE file for details
