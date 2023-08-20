provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repo_name
  format        = "DOCKER"
  description   = var.repo_description
}

resource "google_secret_manager_secret" "secret" {
  secret_id = var.gcp_env_name
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "version" {
  secret      = google_secret_manager_secret.secret.id
  secret_data = file(var.env_file)
}


resource "google_sql_database_instance" "default" {
  name             = var.instance_name
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "default" {
  name       = var.database_name
  instance   = google_sql_database_instance.default.name
}

resource "google_sql_user" "default" {
  name     = var.username
  instance = google_sql_database_instance.default.name
  password = var.password
}

resource "google_cloud_run_service" "default" {
  name     = var.cloud_run_name
  location = var.region

  template {
    spec {
      containers {
        image = "europe-north1-docker.pkg.dev/${var.project_id}/${var.repo_name}/${var.image_name}:latest"
        env {
          name  = "ENVIRONMENT"
          value = "production"
          value_from {
            secret_key_ref {
              name = var.gcp_env_name
              key  = "ENVIRONMENT"
              optional = true
            }
          }
        }
        env {
          name = "HOST_DOMAIN"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "HOST_DOMAIN"
                }
            }
        }
        env {
          name = "FRONTEND_DOMAINS"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "FRONTEND_DOMAINS"
                }
            }
        }
        env {
          name = "POSTGRES_HOST"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "POSTGRES_HOST"
                }
            }
        }
        env {
          name  = "POSTGRES_PORT"
          value = "5432"
          value_from {
            secret_key_ref {
              name = var.gcp_env_name
              key  = "POSTGRES_PORT"
              optional = true
            }
          }
        }
        env {
          name = "POSTGRES_DB"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "POSTGRES_DB"
                }
            }
        }
        env {
          name = "POSTGRES_USER"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "POSTGRES_USER"
                }
            }
        }
        env {
          name = "POSTGRES_PASSWORD"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
                key  = "POSTGRES_PASSWORD"
                }
            }
        }
        env {
          name  = "GUNICORN_WORKERS"
          value = "1"
          value_from {
            secret_key_ref {
              name = var.gcp_env_name
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
              name = var.gcp_env_name
              key  = "SENTRY_DSN"
              optional = true
            }
          }
        }
        env {
          name = "OPENAI_API_KEY"
            value_from {
                secret_key_ref {
                name = var.gcp_env_name
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
