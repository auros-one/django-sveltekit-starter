// Github Actions Service Account
resource "google_service_account" "github_actions_sa" {
  account_id   = "${var.project_slug}-gha"
  display_name = "GitHub Actions Service Account"
  project      = var.project_id

  depends_on = [google_project_service.enable_project_services]
}

// The role required for GitHub Actions to write to Artifact Registry
resource "google_project_iam_binding" "github_actions_artifact_registry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"

  members = [
    "serviceAccount:${google_service_account.github_actions_sa.email}"
  ]
}

// The role required for GitHub Actions to create a new revision of the Cloud Run service
resource "google_project_iam_binding" "github_actions_cloud_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"

  members = [
    "serviceAccount:${google_service_account.github_actions_sa.email}"
  ]
}

// The role required for Github Actions to deploy the new revision of the Cloud Run service
resource "google_project_iam_binding" "github_actions_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"

  members = [
    "serviceAccount:${google_service_account.github_actions_sa.email}"
  ]
}

// A key for the GitHub Actions service account, used to authenticate with Artifact Registry
resource "google_service_account_key" "github_actions_key" {
  service_account_id = google_service_account.github_actions_sa.name
}
