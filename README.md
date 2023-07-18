# django-template

## Setup

### Requirements

-   Python 3.10+
-   Pipenv
-   Docker & Docker Compose

### Installation

Probably a good idea to have stuff working locally for linters, etc.:

```console
pipenv install --dev
```

#### Install pre-commit hooks:

```console
pipenv run pre-commit install
```

### Run the project:

```console
docker compose up -d
docker compose run --rm web manage.py migrate
```

You should be able to access the site at [http://localhost:8000](http://localhost:8000)

### Migrations

```console
docker compose run --rm web manage.py makemigrations
```

### Running management commands

```console
docker compose run --rm web manage.py <command>
```

### Testing

```console
docker compose run --rm web -m pytest --dist=no -n 0 --no-cov
```

**Running a single file**
```console
docker compose run --rm web -m manage shell_plus pytest django_template/app_name/tests.py --dist=no -n 0 --no-cov
```

**generating coverage**

```console
docker compose run --rm web -m pytest --dist=no -n 0 --cov-report=html
```

**Type Checking**

```console
docker compose run --rm web -m mypy
```

## Accounts Verification and Other Emails

We're using dj-rest-auth for authentication which in turn uses django-allauth for email verification. The templates for the emails are overridden in `django_template/accounts/templates/account/email` and the original templates can be found here: https://github.com/pennersr/django-allauth/tree/main/allauth/templates/account/email
