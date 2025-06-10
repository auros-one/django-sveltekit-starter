# Django-SvelteKit Monorepo Merge Instructions

## Overview
You'll be merging two repositories into a single monorepo called `django-sveltekit-starter`:
- Frontend: `github.com/auros-one/sveltekit-template`
- Backend: `github.com/auros-one/backend-template`

**Important**: We want to preserve Git history from both repos!

## Prerequisites
- Git installed and configured
- GitHub CLI (`gh`) installed (optional but helpful)
- Make sure you have push access to the auros-one organization

## Step 1: Create New Repository

1. Create a new repository on GitHub:
   ```bash
   gh repo create auros-one/django-sveltekit-starter --public --description "Production-ready Django + SvelteKit starter template"
   ```

   Or create manually via GitHub UI with name: `django-sveltekit-starter`

2. Clone the new empty repository:
   ```bash
   git clone git@github.com:auros-one/django-sveltekit-starter.git
   cd django-sveltekit-starter
   ```

## Step 2: Merge Backend Repository (Preserving History)

1. Add the backend repo as a remote:
   ```bash
   git remote add backend-template git@github.com:auros-one/backend-template.git
   git fetch backend-template
   ```

2. Merge backend into a subdirectory:
   ```bash
   git merge backend-template/main --allow-unrelated-histories -m "Merge backend-template repository"
   ```

3. Move all backend files into a `backend/` subdirectory:
   ```bash
   # Create the backend directory
   mkdir backend

   # Move all files except .git into backend/
   # This preserves the Git history while reorganizing files
   git ls-tree -r HEAD --name-only | while read filename; do
     if [ -f "$filename" ]; then
       # Create directory structure if needed
       mkdir -p "backend/$(dirname "$filename")"
       git mv "$filename" "backend/$filename"
     fi
   done

   git commit -m "Move backend files into backend/ subdirectory"
   ```

## Step 3: Merge Frontend Repository (Preserving History)

1. Add the frontend repo as a remote:
   ```bash
   git remote add sveltekit-template git@github.com:auros-one/sveltekit-template.git
   git fetch sveltekit-template
   ```

2. Merge frontend into a subdirectory using subtree:
   ```bash
   git read-tree --prefix=frontend/ -u sveltekit-template/main
   git commit -m "Merge sveltekit-template repository into frontend/ subdirectory"

   # Now merge the history
   git pull -s subtree sveltekit-template main --allow-unrelated-histories -m "Merge sveltekit-template history"
   ```

## Step 4: Update Root Configuration Files

1. Create root `.gitignore`:
   ```bash
   cat > .gitignore << 'EOF'
   # IDEs
   .idea/
   .vscode/
   *.swp
   *.swo
   .DS_Store

   # Environment
   .env
   .env.local

   # Dependencies
   node_modules/
   __pycache__/
   *.pyc
   .venv/
   venv/

   # Build outputs
   dist/
   build/
   *.egg-info/

   # Logs
   *.log

   # Docker
   docker-compose.override.yml
   EOF

   git add .gitignore
   git commit -m "Add root .gitignore"
   ```

2. Create root `Makefile`:
   ```bash
   cat > Makefile << 'EOF'
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
   	cd backend && poetry run flake8
   	cd backend && poetry run mypy .
   	cd frontend && npm run lint

   clean:
   	find . -type d -name "__pycache__" -exec rm -rf {} +
   	find . -type f -name "*.pyc" -delete
   	rm -rf frontend/.svelte-kit
   	rm -rf frontend/build
   EOF

   git add Makefile
   git commit -m "Add root Makefile"
   ```

3. Create root `docker-compose.yml`:
   ```bash
   cat > docker-compose.yml << 'EOF'
   version: '3.8'

   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_DB: django_sveltekit_db
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: postgres
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"

     backend:
       build: ./backend
       command: python manage.py runserver 0.0.0.0:8000
       volumes:
         - ./backend:/app
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         DATABASE_URL: postgresql://postgres:postgres@db:5432/django_sveltekit_db
         DEBUG: "True"

     frontend:
       build:
         context: ./frontend
         dockerfile: docker/Dockerfile
       command: npm run dev -- --host
       volumes:
         - ./frontend:/app
         - /app/node_modules
       ports:
         - "5173:5173"
       environment:
         PUBLIC_API_URL: http://localhost:8000
       depends_on:
         - backend

   volumes:
     postgres_data:
   EOF

   git add docker-compose.yml
   git commit -m "Add root docker-compose.yml"
   ```

## Step 5: Update GitHub Actions Workflows

1. Create consolidated workflow structure:
   ```bash
   mkdir -p .github/workflows
   ```

2. Create backend workflow with path filters:
   ```bash
   cat > .github/workflows/backend.yml << 'EOF'
   name: Backend CI/CD

   on:
     push:
       paths:
         - 'backend/**'
         - '.github/workflows/backend.yml'
         - 'docker-compose.yml'
     pull_request:
       paths:
         - 'backend/**'
         - '.github/workflows/backend.yml'
         - 'docker-compose.yml'

   defaults:
     run:
       working-directory: backend

   jobs:
     test:
       runs-on: ubuntu-latest

       services:
         postgres:
           image: postgres:15
           env:
             POSTGRES_PASSWORD: postgres
           options: >-
             --health-cmd pg_isready
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 5432:5432

       steps:
       - uses: actions/checkout@v4

       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.11'

       - name: Install Poetry
         uses: snok/install-poetry@v1
         with:
           virtualenvs-create: true
           virtualenvs-in-project: true

       - name: Load cached venv
         id: cached-poetry-dependencies
         uses: actions/cache@v3
         with:
           path: .venv
           key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}

       - name: Install dependencies
         if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
         run: poetry install --no-interaction --no-root

       - name: Run tests
         env:
           DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
         run: |
           poetry run pytest
           poetry run black --check .
           poetry run isort --check-only .
   EOF

   git add .github/workflows/backend.yml
   ```

3. Create frontend workflow with path filters:
   ```bash
   cat > .github/workflows/frontend.yml << 'EOF'
   name: Frontend CI/CD

   on:
     push:
       paths:
         - 'frontend/**'
         - '.github/workflows/frontend.yml'
         - 'docker-compose.yml'
     pull_request:
       paths:
         - 'frontend/**'
         - '.github/workflows/frontend.yml'
         - 'docker-compose.yml'

   defaults:
     run:
       working-directory: frontend

   jobs:
     test:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v4

       - name: Setup Node.js
         uses: actions/setup-node@v4
         with:
           node-version: '20'
           cache: 'npm'
           cache-dependency-path: frontend/package-lock.json

       - name: Install dependencies
         run: npm ci

       - name: Run linting
         run: npm run lint

       - name: Run type checking
         run: npm run check

       - name: Run tests
         run: npm test

       - name: Build
         run: npm run build
   EOF

   git add .github/workflows/frontend.yml
   ```

4. Create full-stack integration test workflow:
   ```bash
   cat > .github/workflows/integration.yml << 'EOF'
   name: Integration Tests

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     integration:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v4

       - name: Build and start services
         run: |
           docker-compose build
           docker-compose up -d

       - name: Wait for services
         run: |
           timeout 60 bash -c 'until curl -f http://localhost:8000/health/; do sleep 1; done'
           timeout 60 bash -c 'until curl -f http://localhost:5173/; do sleep 1; done'

       - name: Run integration tests
         run: |
           # Add your integration tests here
           curl -f http://localhost:8000/api/
           curl -f http://localhost:5173/

       - name: Show logs on failure
         if: failure()
         run: docker-compose logs

       - name: Stop services
         if: always()
         run: docker-compose down -v
   EOF

   git add .github/workflows/integration.yml
   git commit -m "Add GitHub Actions workflows with path filters"
   ```

## Step 6: Update Configuration Files

1. Update backend Dockerfile path references:
   ```bash
   # If the backend has a Dockerfile, update any COPY commands
   # that might reference parent directories
   sed -i 's|COPY \.\./|COPY |g' backend/Dockerfile 2>/dev/null || true
   ```

2. Update frontend API URL configuration:
   ```bash
   # Update any hardcoded API URLs in frontend to use environment variable
   # This is project-specific, but commonly in:
   # - frontend/src/lib/config.ts
   # - frontend/.env.example
   # - frontend/vite.config.ts
   ```

## Step 7: Create Root Documentation

1. Create comprehensive README:
   ```bash
   cat > README.md << 'EOF'
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
   - Node.js 18+
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
   EOF

   git add README.md
   git commit -m "Add comprehensive README"
   ```

## Step 8: Clean Up and Verify

1. Remove old workflow files if they exist in subdirectories:
   ```bash
   rm -rf backend/.github 2>/dev/null || true
   rm -rf frontend/.github 2>/dev/null || true
   git add -A
   git commit -m "Remove duplicate .github directories" || true
   ```

2. Test the setup:
   ```bash
   # Install dependencies
   make install

   # Try running tests
   make test

   # Try starting development environment
   make dev
   ```

3. Verify Git history is preserved:
   ```bash
   # Should show commits from both original repos
   git log --oneline --graph --all
   ```

4. Push to GitHub:
   ```bash
   git remote remove backend-template
   git remote remove sveltekit-template
   git push -u origin main
   ```

## Step 9: Post-Merge Checklist

- [ ] Both Git histories are preserved
- [ ] `make install` works
- [ ] `make dev` starts both services
- [ ] Frontend can communicate with backend
- [ ] CI/CD workflows trigger correctly on path changes
- [ ] README is accurate and helpful
- [ ] No duplicate configuration files
- [ ] Docker Compose setup works

## Step 10: Archive Old Repositories

Once everything is verified working:

1. Update old repo READMEs to point to new monorepo
2. Archive the original repositories on GitHub
3. Update any documentation/links pointing to old repos

## Troubleshooting

### If Git history merge fails
Use the alternative approach:
```bash
# Create fresh repo and copy files manually
# This loses history but is simpler
cp -r backend-template/* backend/
cp -r sveltekit-template/* frontend/
```

### If Docker Compose has issues
- Check port conflicts
- Ensure environment variables are set
- Verify service dependencies

### If CI/CD doesn't trigger
- Check path filters match your changes
- Ensure workflows have correct permissions
- Verify branch protection rules

## Notes for Future Development

1. **Adding shared packages**: Create a `packages/` directory at root
2. **Deployment**: Consider separate deployment workflows for production
3. **Development**: Always use `make` commands for consistency
4. **Dependencies**: Keep backend and frontend dependencies separate

Good luck with the merge! Test thoroughly at each step.
