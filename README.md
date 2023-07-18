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

```console
docker compose run --rm web -m manage shell_plus pytest home/epcs/tests/test_models.py --dist=no -n 0 --no-cov
docker compose run --rm web -m pytest home/epcs/tests/test_models.py::TestPVParsing --dist=no -n 0 --no-cov
docker compose run --rm web -m pytest home/epcs/tests/test_models.py::TestPVParsing::test_roof_area_regex_valid_string_1 --dist=no -n 0 --no-cov
```

**generating coverage**

```console
docker compose run --rm web -m pytest --dist=no -n 0 --cov-report=html
```

**Type Checking**

```console
docker compose run --rm web -m mypy
```
