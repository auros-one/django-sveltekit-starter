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
          value_from {
            secret_key_ref {
              name = format("%s-env", var.project_slug)
              key  = "ENVIRONMENT"
              optional = true
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
          name = "POSTGRES_HOST"
            value_from {
                secret_key_ref {
                name = format("%s-backend-env", var.project_slug)
                key  = "POSTGRES_HOST"
                }
            }
        }
        env {
          name  = "POSTGRES_PORT"
          value = "5432"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "POSTGRES_PORT"
              optional = true
            }
          }
        }
        env {
          name = "POSTGRES_DB"
            value_from {
                secret_key_ref {
                name = format("%s-backend-env", var.project_slug)
                key  = "POSTGRES_DB"
                default = format("%s-backend-db", var.project_slug)
                }
            }
        }
        env {
          name = "POSTGRES_USER"
            value_from {
                secret_key_ref {
                name = format("%s-backend-env", var.project_slug)
                key  = "POSTGRES_USER"
                default = format("%s-backend-db-user", var.project_slug)
                }
            }
        }
        env {
          name = "POSTGRES_PASSWORD"
            value_from {
                secret_key_ref {
                name = format("%s-backend-env", var.project_slug)
                key  = "POSTGRES_PASSWORD"
                default = var.db_password
                }
            }
        }
        env {
          name  = "GUNICORN_WORKERS"
          value = "1"
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "GUNICORN_WORKERS"
              optional = true
            }
          }
        }
        env {
          name  = "SENTRY_DSN"
          value = ""
          value_from {
            secret_key_ref {
              name = format("%s-backend-env", var.project_slug)
              key  = "SENTRY_DSN"
              optional = true
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
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
