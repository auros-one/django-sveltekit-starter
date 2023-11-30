output "cloud_run_url" {
  description = "The URL of the Cloud Run service."
  value       = google_cloud_run_v2_service.default.uri
}

output "cloud_run_name" {
  description = "The name of the Cloud Run service."
  value       = "${var.project_slug}-cloud-run"
}

output "runtime_dockerimage_url" {
  description = "The URL of the Django Dockerimage."
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.django_repo.name}/${var.project_slug}"
}

output "github_actions_sa_key" {
  description = "The private key of the GitHub Actions service account."
  value       = base64decode(google_service_account_key.github_actions_key.private_key)
  sensitive   = true
}

output "sql_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance."
  value       = google_sql_database_instance.default.connection_name
}
