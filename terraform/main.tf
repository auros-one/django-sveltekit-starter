provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = format("%s-artifact-repo", var.project_slug)
  format        = "DOCKER"
  description   = format("The Artifact Registry of the %s project", var.project_slug)
}

resource "google_secret_manager_secret" "secret" {
  secret_id = format("%s-env", var.project_slug)
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "version" {
  secret      = google_secret_manager_secret.secret.id
  secret_data = file(var.env_file)
}


resource "google_sql_database_instance" "default" {
  name             = format("%s-db", var.project_slug)
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "default" {
  name     = format("%s-backend-db", var.project_slug)
  instance = google_sql_database_instance.default.name
}

resource "google_sql_user" "default" {
  name     = format("%s-backend-db-user", var.project_slug)
  instance = google_sql_database_instance.default.name
  password = var.db_password
}

resource "google_cloud_run_service" "default" {
  name     = format("%s-service", var.project_slug)
  location = var.region

  template {
    spec {
      containers {
        image = format("europe-north1-docker.pkg.dev/${var.project_id}/%s-image/${format("%s-backend-image", var.project_slug)}:latest", var.project_slug)
        env {
          name  = "ENVIRONMENT"
          value = "production"
        }
        env {
          name  = "GUNICORN_WORKERS"
          value = "1"
          value_from {
            secret_key_ref {
              name     = format("%s-backend-env", var.project_slug)
              key      = "GUNICORN_WORKERS"
            }
          }
        }
        env {
          name = "HOST_DOMAIN"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "HOST_DOMAIN"
            }
          }
        }
        env {
          name = "FRONTEND_DOMAINS"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "FRONTEND_DOMAINS"
            }
          }
        }
        env {
          name  = "POSTGRES_HOST"
          value = format("/cloudsql/%s", google_sql_database_instance.default.connection_name)
        }
        env {
          name  = "POSTGRES_PORT"
          value = "5432"
        }
        env {
          name  = "POSTGRES_DB"
          value = google_sql_database.default.name
        }
        env {
          name  = "POSTGRES_USER"
          value = google_sql_user.default.name
        }
        env {
          name = "POSTGRES_PASSWORD"
          value = var.db_password
        }
        env {
          name  = "SENTRY_DSN"
          value = ""
          value_from {
            secret_key_ref {
              name     = format("%s-backend-env", var.project_slug)
              key      = "SENTRY_DSN"
            }
          }
        }
        env {
          name = "OPENAI_API_KEY"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "OPENAI_API_KEY"
            }
          }
        }
        env {
          name  = "HELICONE_API_KEY"
          value = ""
          value_from {
            secret_key_ref {
              name     = format("%s-backend-env", var.project_slug)
              key      = "HELICONE_API_KEY"
            }
          }
        }
        env {
          name = "CLOUDRUN_SERVICE_URL"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "CLOUDRUN_SERVICE_URL"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}


/*
This resource grants public access to the Cloud Run service by assigning the 'roles/run.invoker' role to 'allUsers'.
-> This means any authenticated or unauthenticated user can invoke (access) the service.
This configuration is equivalent to using the --allow-unauthenticated option in the gcloud run deploy command
*/
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}


resource "google_service_account" "github_actions" {
  account_id   = lower(replace(format("%s-backend-ga", var.project_slug), "_", "-"))
  display_name = format("GitHub Actions service account for the %s backend", var.project_slug)
  description  = format("The service account used by the GitHub Actions of the %s backend to deploy from its ci.yml", var.project_slug)
}

resource "google_project_iam_member" "github_actions_roles" {
  for_each = toset([
    "roles/artifactregistry.writer",
    "roles/cloudsql.admin",
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

resource "google_service_account_key" "github_actions_key" {
  service_account_id = google_service_account.github_actions.name
}
