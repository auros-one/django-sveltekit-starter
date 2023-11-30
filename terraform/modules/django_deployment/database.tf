resource "google_sql_database_instance" "default" {
  name             = "${var.project_slug}-db-instance"
  database_version = "POSTGRES_15"
  project          = var.project_id
  region           = var.region

  // to destroy the database instance, set this to trueP
  deletion_protection = false

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      private_network = "projects/${var.project_id}/global/networks/default"
    }
  }

  depends_on = [google_project_service.enable_project_services, google_service_networking_connection.private_vpc_connection]
}

resource "google_sql_database" "db" {
  name     = "${var.project_slug}-db"
  instance = google_sql_database_instance.default.name
  project  = var.project_id
}

resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "google_sql_user" "default_user" {
  name     = "default"
  instance = google_sql_database_instance.default.name
  password = random_password.db_password.result
  project  = var.project_id
}

output "db_private_ip" {
  value = google_sql_database_instance.default.private_ip_address
}

output "db_name" {
  value = google_sql_database.db.name
}

output "db_user" {
  value = google_sql_user.default_user.name
}

output "db_password" {
  value = random_password.db_password.result
}
