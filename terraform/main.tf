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

resource "google_cloud_run_service" "default" {
  name     = var.cloud_run_name
  location = var.region

  template {
    spec {
      containers {
        image = "europe-north1-docker.pkg.dev/${var.project_id}/${var.repo_name}/${var.image_name}:latest"
        envs {
          name  = "ENV_FILE"
          value = "/app/secrets/.env"
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
