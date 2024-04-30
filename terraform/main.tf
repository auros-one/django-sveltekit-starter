
// We use GCS as a backend for storing the state of our infrastructure.
terraform {
  backend "gcs" {
    bucket = ""
    prefix = "terraform/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.1.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">=3.5.1"
    }
  }

  required_version = ">= 1.4.6"
}


// Django deployment module

module "django_deployment" {
  source          = "./modules/django_deployment"
  project_id      = ""
  region          = "us-east4"
  project_slug    = ""
  sentry_dsn      = ""
  frontend_domain = ""
  mailgun_api_key = ""
  mailgun_sender_domain = ""
}

// Output the values of the outputs from the Django deployment module

output "cloud_run_url" {
  value       = module.django_deployment.cloud_run_url
  description = "The URL of the Cloud Run service."
}

output "cloud_run_name" {
  value       = module.django_deployment.cloud_run_name
  description = "The name of the Cloud Run service."
}

output "runtime_dockerimage_url" {
  value       = module.django_deployment.runtime_dockerimage_url
  description = "The URL of the Django Dockerimage."
}

output "sql_instance_connection_name" {
  value       = module.django_deployment.sql_instance_connection_name
  description = "The connection name of the Cloud SQL instance."
}

output "github_actions_sa_key" {
  value       = module.django_deployment.github_actions_sa_key
  description = "The private key of the GitHub Actions service account."
  sensitive   = true
}
