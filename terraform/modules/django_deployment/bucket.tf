resource "google_storage_bucket" "gcs_bucket" {
  name     = "${var.project_id}-gcr-bucket"
  location = var.region
  project  = var.project_id

  // Uniform bucket-level access is enabled required for the public access
  uniform_bucket_level_access = true

  cors {
    origin          = ["https://${var.frontend_domain}"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  depends_on = [google_project_service.enable_project_services]
}

// Allow public read access to the bucket
resource "google_storage_bucket_iam_binding" "public_read" {
  bucket = google_storage_bucket.gcs_bucket.name
  role   = "roles/storage.objectViewer"

  members = [
    "allUsers",
  ]
}

output "gcs_bucket_name" {
  value = google_storage_bucket.gcs_bucket.name
}
