// Cloud Run Service Account
resource "google_service_account" "cloud_run_sa" {
  account_id   = "${var.project_slug}-run"
  display_name = "Cloud Run Service Account"
  project      = var.project_id

  depends_on = [google_project_service.enable_project_services]
}

// Role required for Cloud Run service to interact with Cloud SQL
resource "google_project_iam_binding" "cloud_run_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.cloud_run_sa.email}"
  ]
}

// Role required for Cloud Run service to interact with GCS bucket
resource "google_project_iam_binding" "cloud_run_gcs_access" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"

  members = [
    "serviceAccount:${google_service_account.cloud_run_sa.email}"
  ]
}

// Role required for Cloud Run service to read from Secret Manager
resource "google_project_iam_binding" "cloud_run_secret_manager_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.cloud_run_sa.email}"
  ]
}


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

// The role required for GitHub Actions to write to Artifact Registry
resource "google_project_iam_binding" "github_actions_cloud_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"

  members = [
    "serviceAccount:${google_service_account.github_actions_sa.email}"
  ]
}

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
