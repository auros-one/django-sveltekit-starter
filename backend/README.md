# Django Template

Django template with multiple convenient features.

Authentication integration with the SvelteKit Template.

## Local Development

### Requirements

-   Python 3.11+
-   Poetry
-   Docker & Docker Compose

### Installation

```console
cp .env.example .env
poetry install
poetry shell
pre-commit install
```

### Running Locally

**Don't forget to activate the Python virtual environment with `poetry shell`**

**start DB and run migrations**

```console
docker compose up db -d
poetry shell
python manage.py migrate
```

**run development server**

```console
python manage.py runserver
```

### Running in docker compose

```console
docker compose up -d
docker compose run --rm web python manage.py migrate
```

### Migrations

```console
python manage.py makemigrations
python manage.py migrate
```

### Testing

**in Poetry**

```console
pytest --dist=no -n 0 --cov-report=html
```

**Running a specific file**

```console
docker compose run --rm web python -m pytest project/app_name/tests.py --dist=no -n 0 --cov-report=html
```

**Test Coverage**

By running the tests with `--cov-report=html` a coverage report will be generated in `htmlcov/index.html`.

**in Docker**

```console
docker compose run --rm web python -m pytest --dist=no -n 0 --cov-report=html
```

### Type Checking

```console
pyright .
```

## Django Management Commands

```console
python manage.py <command>
```

## Accounts Verification and Other Emails

We're using dj-rest-auth for authentication which in turn uses django-allauth for email verification. The templates for the emails are overridden in `project/accounts/templates/account/email` and the original templates can be found here: https://github.com/pennersr/django-allauth/tree/main/allauth/templates/account/email

## Deployment

See [DEPLOY.md](/DEPLOY.md) for deployment instructions.

Once the deployment setup is complete, Github Actions will automatically deploy changes to main to the server.

## Running Celery Worker

To start the Celery worker with the correct queue configuration:

```console
# Activate virtual environment first

# Start the Celery worker
celery -A project worker --loglevel=info -Q default
```

This ensures the worker only processes tasks meant for the application.
