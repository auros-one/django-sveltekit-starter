resource "google_secret_manager_secret" "config" {
  project   = var.project_id
  secret_id = "${var.project_slug}-config"
  replication {
    auto {} // The Secret will automatically be replicated accross regions without any restrictions.
  }

  depends_on = [google_project_service.enable_project_services]
}

resource "random_password" "django_secret" {
  length  = 60
  special = false
}

// Cloud Run mounts the secret as a volume so a version must be present to create it.
resource "google_secret_manager_secret_version" "placeholder_config" {
  secret      = google_secret_manager_secret.config.id
  secret_data = "placeholder .env"
}

// The actual config is created after the Cloud Run service is created.
resource "google_secret_manager_secret_version" "config" {
  secret      = google_secret_manager_secret.config.id
  secret_data = <<-EOF
    POSTGRES_HOST=/cloudsql/${google_sql_database_instance.default.connection_name}
    POSTGRES_DB=${google_sql_database.db.name}
    POSTGRES_USER=${google_sql_user.default_user.name}
    POSTGRES_PASSWORD=${random_password.db_password.result}

    GS_BUCKET_NAME=${google_storage_bucket.gcs_bucket.name}

    DEBUG=0
    ENVIRONMENT=production
    GUNICORN_RELOAD=0
    GUNICORN_WORKERS=1
    SECRET_KEY=${random_password.django_secret.result}
    SENTRY_DSN=${var.sentry_dsn}
    HOST_DOMAIN=${replace(google_cloud_run_v2_service.default.uri, "https://", "")}
    FRONTEND_DOMAIN=${var.frontend_domain}

    MAILGUN_API_KEY=${var.mailgun_api_key}
    MAILGUN_SENDER_DOMAIN=${var.mailgun_sender_domain}
EOF
}

output "secret_manager_config_version" {
  value = google_secret_manager_secret_version.config.name
}
