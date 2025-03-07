# Backend Deployment with Ansible and Dokku

This directory contains Ansible playbooks for deploying the JobFunnel backend application using Dokku on a Hetzner Cloud server.

## Overview

This Ansible project automates the deployment of a Django backend application to a Hetzner Cloud server using Dokku, a lightweight PaaS (Platform as a Service) that simplifies application deployment. The playbooks handle everything from installing Dokku to configuring the application environment, database, and SSL certificates.

## Project Structure

```
ansible/
├── group_vars/           # Common variables for all hosts
│   └── all.yml           # Variables loaded from ansible_env.yml
├── inventory/            # Server inventory definitions
│   └── hosts             # Target server configuration
├── roles/                # Modular deployment roles
│   ├── dokku_base/       # Dokku installation and setup
│   ├── dokku_database/   # PostgreSQL database configuration
│   ├── dokku_redis/      # Redis configuration
│   ├── dokku_application/# Application setup and configuration
│   └── dokku_environment/# Environment variables and domain setup
├── ansible_env.yml       # Configuration variables (create this file)
├── README.md             # This documentation
└── site.yml              # Main playbook that orchestrates all roles
```

## How It Works

The deployment process is organized into four sequential roles, each handling a specific aspect of the deployment:

1. **dokku_base**: Installs and configures Dokku on the server
   - Installs required dependencies (apt-transport-https, git, etc.)
   - Downloads and runs the Dokku bootstrap script (v0.30.7)
   - Installs essential Dokku plugins:
     - PostgreSQL plugin for database management
     - Redis plugin for Celery message broker
     - Let's Encrypt plugin for SSL certificates

2. **dokku_database**: Sets up and configures the PostgreSQL database
   - Creates a PostgreSQL database service with the specified version
   - Exposes the PostgreSQL port (5432) for external access
   - Configures S3 credentials for automated database backups
   - Sets up daily short-term backups (expire after 7 days)
   - Sets up weekly long-term backups (expire after 30 days)
   - Installs and configures MinIO client for managing S3 bucket lifecycle rules

3. **dokku_redis**: Sets up and configures Redis for Celery
   - Creates a Redis service if it doesn't exist
   - Links the Redis service to the application
   - Ensures Dokku uses the Procfile from the repository

4. **dokku_application**: Creates and configures the Dokku application
   - Creates the Dokku application if it doesn't exist
   - Configures Dokku to use the Dockerfile from the project root
   - Links the PostgreSQL database to the application

5. **dokku_environment**: Sets up the application environment
   - Copies the `.env` file from the project root to the server
   - Sets environment variables in Dokku from the `.env` file
   - Sets computed environment variables (HOST_DOMAINS, ALLOWED_HOSTS)
   - Configures domain names for the application
   - Sets up Let's Encrypt for HTTPS
   - Restarts the application to apply all changes

## Configuration

### 1. Create ansible_env.yml File

Create an `ansible_env.yml` file in the ansible directory with your specific values. This file is loaded by `group_vars/all.yml` and provides all the configuration variables needed for deployment.

### 2. Update Inventory File

Update the `inventory/hosts` file with your server's IP address:

```ini
[app_server]
app ansible_host=your-server-ip ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_ssh_common_args='-o ForwardAgent=yes -o StrictHostKeyChecking=no'

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### 3. Configure Your .env File

Ensure your project's `.env` file at the root of the repository contains all required environment variables for your application. This file will be copied to the server and used to configure the application in Dokku.

## Running the Deployment

To deploy the application:

```bash
cd ansible
ansible-playbook -i inventory/hosts site.yml
```

For a dry run (to see what would change without making changes):

```bash
ansible-playbook -i inventory/hosts site.yml --check
```

For more detailed output:

```bash
ansible-playbook -i inventory/hosts site.yml -v
```

## Accessing the Deployed Application

### Backend API

After deployment, your backend API will be available at:

```
https://api.your-domain.com
```

### Celery Flower

Celery Flower provides a web interface for monitoring and administering Celery tasks and workers. After deployment, it will be available at:

```
https://api.your-domain.com/flower
```

You can log in using the credentials specified in the `FLOWER_BASIC_AUTH` environment variable (default: admin:admin).

### Celery Beat

Celery Beat is a scheduler that triggers periodic tasks at specified intervals. After deployment, it will be running as a separate process. You can configure periodic tasks through the Django admin interface at:

```
https://api.your-domain.com/admin/django_celery_beat/
```

### PostgreSQL Database

The PostgreSQL database is exposed on port 5432 and can be accessed using:

```bash
# Get database connection information
ssh root@your-server-ip dokku postgres:info jobfunnel-db

# Connect to the database using psql
ssh root@your-server-ip dokku postgres:connect jobfunnel-db
```

For external access (e.g., from your local machine):

```bash
# Get the database credentials
ssh root@your-server-ip dokku postgres:info jobfunnel-db

# Connect using psql from your local machine
psql -h your-server-ip -p 5432 -U postgres -d jobfunnel-db
```

## Checking Deployment Status

To check the status of your application:

```bash
ansible -i inventory/hosts app_server -m shell -a "dokku ps:report jobfunnel-backend"
```

To view logs:

```bash
ansible -i inventory/hosts app_server -m shell -a "dokku logs jobfunnel-backend -t"
```

To check Celery worker status:

```bash
ansible -i inventory/hosts app_server -m shell -a "dokku ps:report jobfunnel-backend worker"
```

## Troubleshooting

If you encounter issues during deployment:

1. Check the Ansible output for error messages
2. Verify that your `ansible_env.yml` file contains the correct values
3. Ensure your `.env` file is properly configured
4. Check that you can SSH into the server manually: `ssh root@your-server-ip`
5. Verify that Dokku is installed: `ssh root@your-server-ip dokku version`
6. Check the Dokku logs: `ssh root@your-server-ip dokku logs jobfunnel-backend -t`
7. Verify the database service is running: `ssh root@your-server-ip dokku postgres:info jobfunnel-db`
8. Check the application configuration: `ssh root@your-server-ip dokku config jobfunnel-backend`

## Advanced Configuration

The deployment can be customized by editing the respective role files:

- `roles/dokku_base/tasks/main.yml` - For Dokku installation settings
- `roles/dokku_database/tasks/main.yml` - For database configuration
- `roles/dokku_redis/tasks/main.yml` - For Redis configuration
- `roles/dokku_application/tasks/main.yml` - For application setup
- `roles/dokku_environment/tasks/main.yml` - For environment configuration
- `group_vars/all.yml` - For common variables
