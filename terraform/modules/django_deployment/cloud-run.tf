
/*
* We use a null_resource to push a placeholder image to the artifact
* repository when it's created. Otherwise we can't deploy the Cloud Run.
*
* It only pushes the placeholder image if there are no images in
* the repository.
*
* The CI/CD pipeline will push the real image to the Artifact Repo and
* deploy it to Cloud Run.
*/
resource "null_resource" "push_placeholder_image_if_needed" {
  triggers = {
    repo_name = google_artifact_registry_repository.django_repo.name
  }

  provisioner "local-exec" {
    command = <<EOT
      REPO_NAME="${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.django_repo.name}"
      IMAGE_TAG="$REPO_NAME/${var.project_slug}:latest"

      # Authenticate Docker with gcloud
      gcloud auth configure-docker ${var.region}-docker.pkg.dev

      # Check if any image exists in the repository
      if ! gcloud artifacts docker images list "$REPO_NAME" --format='get(tags)' | grep -q 'latest'; then
        docker pull ${var.placeholder_image}
        docker tag ${var.placeholder_image} "$IMAGE_TAG"
        docker push "$IMAGE_TAG"
      fi
    EOT
  }

  depends_on = [
    google_artifact_registry_repository.django_repo
  ]
}


resource "google_cloud_run_v2_service" "default" {
  name     = "${var.project_slug}-cloud-run"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloud_run_sa.email
    volumes {
      name = "secret-config"
      secret {
        secret       = google_secret_manager_secret.config.secret_id
        default_mode = 292 # = 0444 = readonly
        items {
          version = "latest"
          path    = ".env"
        }
      }
    }
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.default.connection_name]
      }
    }
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.django_repo.name}/${var.project_slug}:latest"
      volume_mounts {
        name       = "secret-config"
        mount_path = "/app/secrets" // Django will look for the .env file in this directory (see settings.py)
      }
      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
      resources {
        limits = {
          cpu    = "1000m"
          memory = "800Mi"
        }
      }
    }
    max_instance_request_concurrency = 50
  }

  depends_on = [null_resource.push_placeholder_image_if_needed, google_project_service.enable_project_services, google_secret_manager_secret_version.placeholder_config]
}

resource "google_cloud_run_service_iam_member" "cloud_run_invoker" {
  service  = google_cloud_run_v2_service.default.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}
