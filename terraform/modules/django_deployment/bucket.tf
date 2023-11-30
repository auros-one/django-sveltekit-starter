resource "google_storage_bucket" "gcs_bucket" {
  name     = "${var.project_id}-gcr-bucket"
  location = var.region
  project  = var.project_id

  cors {
    origin          = ["https://${var.frontend_domain}"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  depends_on = [google_project_service.enable_project_services]
}

output "gcs_bucket_name" {
  value = google_storage_bucket.gcs_bucket.name
}
