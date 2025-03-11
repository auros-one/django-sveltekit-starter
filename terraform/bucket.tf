resource "minio_s3_bucket" "app_media" {
  bucket = "${var.project_name}-app-media"
  acl    = "public-read"

  lifecycle {
    ignore_changes = all
    prevent_destroy = true
  }
}

resource "minio_s3_bucket" "db_backups" {
  bucket = "${var.project_name}-db-backups"
  acl    = "private"

  lifecycle {
    ignore_changes = all
    prevent_destroy = true
  }
}
