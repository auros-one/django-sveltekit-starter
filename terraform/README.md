# Infrastructure as Code

This Terraform configuration defines the infrastructure for a Django application on Hetzner Cloud. The infrastructure supports a Django backend application with PostgreSQL database using Dokku for containerized deployment.

## Project Structure

The Terraform project is organized into several files, each with a specific purpose:

- **main.tf**: Core configuration file that defines:
  - Required providers (Hetzner Cloud and MinIO)
  - Provider configuration with authentication details
  - SSH key resources for server access
  - Main server resource with labels and configuration

- **variables.tf**: Defines all input variables used throughout the configuration:
  - API tokens and credentials
  - Server location and type
  - Project name and environment
  - S3 endpoint configuration
  - Developer SSH keys

- **network.tf**: Configures the private network infrastructure:
  - Private network (10.0.0.0/16) for internal communication
  - Subnet in the eu-central network zone
  - Server network attachment with static IP (10.0.1.1)

- **firewall.tf**: Sets up firewall rules to secure the server:
  - HTTP (80) and HTTPS (443) for web traffic
  - SSH (22) for secure server access
  - PostgreSQL (5432) for database access with IP restrictions

- **bucket.tf**: Configures S3 buckets for application storage:
  - Media bucket (`$PROJECT_NAME-app-media`) with public-read ACL
  - Backup bucket (`$PROJECT_NAME-db-backups`) with private ACL

- **outputs.tf**: Defines output values that are displayed after infrastructure creation:
  - Server IP address and status
  - SSH command for server access
  - Dokku setup URL
  - S3 bucket names and endpoints

## Infrastructure Components

### Server

The configuration creates a single Ubuntu 22.04 server (CPX21 by default) running Dokku, which hosts:
- The Django backend application
- PostgreSQL database as a Dokku service
- Both components are deployed as separate Dokku apps

Server features:
- Configured with developer SSH keys for secure access
- Tagged with labels for project, environment, and application roles
- Sized appropriately for production workloads (CPX21 has 4 vCPUs, 8GB RAM)

### Network

A private network is created for secure internal communication:
- Network range: 10.0.0.0/16
- Subnet: 10.0.1.0/24 in the eu-central network zone
- Server attached with static IP: 10.0.1.1

### Firewall

A firewall is configured to secure the server with the following rules:
- HTTP (80) and HTTPS (443) open to the internet for web access
- SSH (22) open to the internet for administrative access
- PostgreSQL (5432) restricted to specified IPs for database security

### S3 Storage

Two S3 buckets are configured for application storage:
- Media bucket (`$PROJECT_NAME-app-media`): Stores user-uploaded files with public-read ACL
- Backup bucket (`$PROJECT_NAME-db-backups`): Stores database backups with private ACL

## Configuration

All configuration is done through variables in `terraform.tfvars`. The key variables include:

- **hcloud_token**: Hetzner Cloud API token for authentication
- **hetzner_s3_access_key/secret_key**: Credentials for S3 object storage
- **domain_name**: Domain name for the application
- **server_location**: Hetzner datacenter location (e.g., "nbg1" for Nuremberg)
- **project_name**: Name used for resource naming and tagging
- **s3_endpoint_url**: Endpoint URL for Hetzner S3 storage
- **developer_ssh_keys**: Map of developer names to their SSH public keys

## Important Notes

### Backend Environment Variables

The backend application relies on environment variables that are set during the Ansible deployment process. The `dokku_environment/tasks/main.yml` file copies the backend's `.env` file to the server and configures these variables in Dokku.

**It is critical that your backend's `.env` file is properly configured before running the Ansible deployment**, as these variables will be used to:

1. Configure the application's connection to the database
2. Set up S3 storage access
3. Configure domain settings and SSL certificates
4. Set other application-specific variables

### SSH Keys

The SSH keys defined in the `developer_ssh_keys` variable are automatically uploaded to Hetzner Cloud and configured on the server. Each developer's public key is registered in Hetzner Cloud and attached to the server, allowing them to use their corresponding private key (e.g., `~/.ssh/id_rsa`) to SSH into the server.

## Terraform State

The Terraform state is stored locally by default. For team environments, consider:
- Using a remote state backend like Terraform Cloud
- Implementing state locking for collaborative work
- Backing up the state file regularly