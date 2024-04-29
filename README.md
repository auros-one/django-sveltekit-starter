# Django Template

Django template with multiple convenient features.

Authentication integration with the SvelteKit Template.

## Local Development

### Requirements

-   Python 3.11+
-   Pipenv
-   Docker & Docker Compose

### Installation

```console
cp .env.example .env
pipenv install --dev
pipenv shell
pre-commit install
```

### Running Locally

**Don't forget to activate the Python virtual environment with `pipenv shell`**

**start DB and run migrations**

```console
docker compose up db -d
pipenv shell
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

**in Pipenv**

```console
pytest --dist=no -n 0 --cov-report=html
```

**Running a specific file**

```console
docker compose run --rm web python -m manage shell_plus pytest project/app_name/tests.py --dist=no -n 0 --cov-report=html
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

### Deploy with Terraform

[Terraform Deployment Instructions](/terraform/README.md) - After deploying the infrastructure with Terraform, let the CI/CD pipeline deploy the Django application to this infrastracture (Cloud Run).

### Setting up GitHub Actions CI/CD

**Store the following Terraform outputs as [Github Repository Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository):**

-   Terraform output `runtime_dockerimage_url` -> Github Repo Secret `RUNTIME_DOCKERIMAGE_URL`
-   Terraform output `github_actions_sa_key` -> Github Repo Secret `GOOGLE_AUTHENTICATION_CREDENTIALS_JSON`
-   Terraform output `cloud_run_id` -> Github Repo Secret `CLOUD_RUN_NAME`

View a Terraform secret with:

```console
terraform output <secret_name>
```

### Post-Deployment Settings

Don't forget to:

-   create a superuser
-   set the site name and domain

The 'Managing the Django deployment' section below has instructions on how to do this.

## Managing the Django deployment

**ALWAYS FIRST SET THE ENV VARS AND AUTHENTICATE TO GCP**

```console
export PROJECT_ID= ... # GCP Project ID
export PROJECT_SLUG= ... # GCP Project slug (this is one of the Terraform module inputs)
export CLOUD_SQL_CONNECTION_NAME = ... # GCP Cloud SQL connection name (this is one of the Terraform module outputs)
export RUNTIME_DOCKERIMAGE_URL= ... # Terraform output `runtime_dockerimage_url`
CLOUD_RUN_NAME= ... # Terraform output `cloud_run_name`
```

```console
gcloud auth login
gcloud auth application-default login
gcloud config set project $PROJECT_ID
```

### Creating a Superuser

1. Set the database connection details in your `.env` (see below how to get the GCP .env.gcp file to get the DB connection details).

```
POSTGRES_HOST=localhost
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

2. Connect to the Cloud SQL using the Cloud SQL Proxy.
    - See [Connecting from a local machine](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#connect) for information on setting up the proxy.
    - See `terraform output` to get the `sql_instance_connection_name`

```console
./cloud-sql-proxy $CLOUD_SQL_CONNECTION_NAME
// Example:
./cloud-sql-proxy "test-deployment-2-405517:europe-north1:deployment-twee-db-instance"
```

3. Create a superuser using the Django command.

```console
python manage.py createsuperuser
```

### Setting Site Name and Domain

Don't forget to update the site domain and name in the Django backend at:

-   url: <terraform output `cloud_run_url`>/admin/sites/site

This name and domain are used in the email templates and the admin dashboard.
cloud_run_url

### Editing .env.gcp

**Get the current .env.gcp file**:

```console
gcloud secrets versions access latest --secret="$PROJECT_SLUG-config" --project="$PROJECT_ID" > .env.gcp
```

**Set a new .env.gcp file**:

```console
gcloud secrets versions add "$PROJECT_SLUG-config" --data-file=".env.gcp"
```

**List all versions of the .env.gcp file**:

```console
gcloud secrets versions list "$PROJECT_SLUG-config"
```

**Required project details:**

```console
export PROJECT_ID= ... # GCP project ID
export RUNTIME_DOCKERIMAGE_URL= ... # Terraform output `runtime_dockerimage_url`
```

**Authenticate to GCP**

```console
gcloud auth login
gcloud auth application-default login
gcloud config set project $PROJECT_ID
```

### Deploying manually

```console
export DOCKER_IMG="${RUNTIME_DOCKERIMAGE_URL}:latest"
docker buildx build \
  --platform linux/amd64 \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -f Dockerfile \
  --no-cache \
  -t $DOCKER_IMG \
  .
docker push $DOCKER_IMG
gcloud run deploy $CLOUD_RUN_NAME \
  --image=$DOCKER_IMG \
  --region=europe-north1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-secrets=/app/secrets/.env=$PROJECT_SLUG-config:latest
```
