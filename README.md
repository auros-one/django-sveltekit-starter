# Django Template

Django template with multiple convenient features.

Authentication integration with the SvelteKit Template.

## Setup

### Requirements

-   Python 3.10+
-   Pipenv
-   Docker & Docker Compose

### Cloning the template

Search the project files (CTRL+SHIFT+F) and replace all instances of `project_name` with your project name (using the same snake_case style).

### Installation

**using pipenv**

```console
cp .env.example .env
pipenv install --dev
pipenv run pre-commit install
```

## Running

**setup**

```console
docker compose up db -d
pipenv run python manage.py migrate
```

**run**

```console
pipenv run python manage.py runserver
```

### Running in docker compose

```console
docker compose up -d
docker compose run --rm web manage.py migrate
```

## Deployment


**Site Name and Domain**

Don't forget to update the site domain and name at https://<your-domain>/admin/sites/site

This name and domain are used in the email templates and the Django admin dashboard.

# Testing

```console
docker compose run --rm web -m pytest --dist=no -n 0 --no-cov
```

**Running a single file**

```console
docker compose run --rm web -m manage shell_plus pytest project/app_name/tests.py --dist=no -n 0 --no-cov
```

**generating coverage**

```console
docker compose run --rm web -m pytest --dist=no -n 0 --cov-report=html
```

**Type Checking**

```console
docker compose run --rm web -m mypy
```

# Django

## Migrations

```console
docker compose run --rm web manage.py makemigrations
```

## Running management commands

```console
docker compose run --rm web manage.py <command>
```

## Accounts Verification and Other Emails

We're using dj-rest-auth for authentication which in turn uses django-allauth for email verification. The templates for the emails are overridden in `project/accounts/templates/account/email` and the original templates can be found here: https://github.com/pennersr/django-allauth/tree/main/allauth/templates/account/email
