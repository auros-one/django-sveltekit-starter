terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = ">= 1.46.1"
    }
    minio = {
      source  = "aminueza/minio"
      version = "3.2.2"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

provider "minio" {
  minio_server   = var.minio_server_url
  minio_user     = var.hetzner_s3_access_key
  minio_password = var.hetzner_s3_secret_key
  minio_region   = var.server_location
  minio_ssl      = true
}

# Single server hosting both backend and database as separate Dokku apps
resource "hcloud_server" "app_server" {
  name        = "${var.project_name}-app"
  server_type = var.server_type
  image       = var.server_image
  location    = var.server_location

  labels = {
    role        = "application"
    project     = var.project_name
    environment = "production"
    dokku_apps  = "backend-database"  # Using dash instead of comma
  }

  # Prevent server replacement when SSH keys change
  lifecycle {
    ignore_changes = [
      ssh_keys
    ]
  }
}
