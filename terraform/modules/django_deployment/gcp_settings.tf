
variable "apis_to_enable" {
  description = "List of Google Cloud APIs to enable"
  type        = list(string)
  default     = [
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "storage-component.googleapis.com",
    "servicenetworking.googleapis.com",
    "compute.googleapis.com",
  ]
}

resource "google_project_service" "enable_project_services" {
  for_each = toset(var.apis_to_enable)

  project = var.project_id
  service = each.key

  disable_dependent_services = true
  disable_on_destroy         = false
}

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
