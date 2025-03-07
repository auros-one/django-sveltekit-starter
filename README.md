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

[Terraform Deployment Instructions](/terraform/README.md) - Terraform creates the infrastructure on Hetzner Cloud including server, network, firewall, and S3 buckets. Run `terraform apply` in the terraform directory to provision all resources.

### Deploying to Hetzner Cloud with Dokku

For deploying to our Hetzner Cloud infrastructure using Dokku, we use a dedicated GitHub Actions workflow:

1. **Automatic Deployment**: The workflow in `.github/workflows/deploy-to-dokku.yml` automatically deploys any code pushed to the `hetzner` branch to our Dokku application.

2. **How to Deploy**:
   ```console
   git checkout hetzner
   git add .
   git commit -m "Your changes"
   git push origin hetzner
   ```

### Ansible Deployment

After Terraform creates the infrastructure, Ansible configures the server:

```console
cd ansible
ansible-playbook -i inventory/hosts site.yml
```

This installs Dokku, sets up PostgreSQL, configures the application, and manages environment variables. See [Deployment Guide](/deploy.md) for details.

### Setting up GitHub Actions CI/CD for Dokku

To set up the GitHub Actions workflow for automatic deployment to Dokku:

1. **Configure the following secrets in your GitHub repository**:
   - `DOKKU_GIT_REMOTE_URL`: The Git remote URL for your Dokku app (format: `ssh://dokku@your-server-ip:your-project-name-backend`)
   - `DOKKU_SSH_PRIVATE_KEY`: The SSH private key that has access to your Dokku server

2. **Verify the workflow file**:
   - Ensure `.github/workflows/deploy-to-dokku.yml` is configured to deploy from the `hetzner` branch

### Post-Deployment Settings

After deployment, you'll need to configure a few settings:

1. **Create a superuser**:
   ```console
   # SSH into your server
   ssh root@your-server-ip

   # Create a superuser
   dokku run your-project-name-backend python manage.py createsuperuser
   ```

2. **Configure site domain**:
   - Access the Django admin at `https://api.your-domain.com/admin/sites/site/`
   - Update the domain to match your actual domain

For more detailed instructions, see the [Deployment Guide](/deploy.md).

## Managing Your Dokku Deployment

### Useful Commands

```console
# View application logs
ssh root@your-server-ip dokku logs your-project-name-backend -t

# Restart the application
ssh root@your-server-ip dokku ps:restart your-project-name-backend

# View environment variables
ssh root@your-server-ip dokku config your-project-name-backend

# Set an environment variable
ssh root@your-server-ip dokku config:set your-project-name-backend KEY=VALUE

# Access PostgreSQL database
ssh root@your-server-ip dokku postgres:connect your-project-name-db
```

### Manual Deployment

If you need to deploy manually (without GitHub Actions):

```console
# Add the Dokku remote
git remote add dokku dokku@your-server-ip:your-project-name-backend

# Push your changes
git push dokku main:master
```

For complete documentation on managing your deployment, refer to the [Deployment Guide](/deploy.md).

## Running Celery Worker

To start the Celery worker with the correct queue configuration:

`ash
# Activate virtual environment first

# Start the Celery worker
celery -A project worker --loglevel=info -Q backend_tasks
``n
This ensures the backend worker only processes tasks meant for the backend application.
