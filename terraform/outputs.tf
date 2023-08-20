output "artifact_registry_url" {
  description = "The URL of the Artifact Registry repository."
  value       = google_artifact_registry_repository.repo.location
}

output "secret_version" {
  description = "The version of the secret in GCP Secret Manager."
  value       = google_secret_manager_secret_version.version.name
}

output "cloud_run_url" {
  description = "The URL of the Cloud Run service."
  value       = google_cloud_run_service.default.status[0].url
}

output "sql_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance."
  value       = google_sql_database_instance.default.connection_name
}

output "github_actions_sa_key" {
  description = "The private key of the GitHub Actions service account."
  value       = google_service_account_key.github_actions_key.private_key
  sensitive   = true
}
