resource "google_artifact_registry_repository" "django_repo" {
  repository_id = "${var.project_slug}-docker-repo"
  location      = var.region
  project       = var.project_id
  format        = "DOCKER"

  depends_on = [google_project_service.enable_project_services]
}

data "google_iam_policy" "artifact_registry_policy" {
  binding {
    role = "roles/artifactregistry.writer"

    members = [
      "serviceAccount:${google_service_account.github_actions_sa.email}"
    ]
  }
}

resource "google_artifact_registry_repository_iam_policy" "django_repo_iam_policy" {
  repository  = google_artifact_registry_repository.django_repo.name
  location    = var.region
  policy_data = data.google_iam_policy.artifact_registry_policy.policy_data
}
