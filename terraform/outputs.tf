output "server_ip" {
  description = "Public IP address of the server"
  value       = hcloud_server.app_server.ipv4_address
}

output "server_status" {
  description = "Status of the server"
  value       = hcloud_server.app_server.status
}


output "hetzner_s3_access_key" {
  description = "Access key for the Hetzner S3 bucket"
  value       = var.hetzner_s3_access_key
}

output "hetzner_s3_secret_key" {
  description = "Secret key for the Hetzner S3 bucket"
  value       = var.hetzner_s3_secret_key
}

output "hetzner_s3_bucket_name" {
  description = "Endpoint URL for the S3 bucket for application media files"
  value       = minio_s3_bucket.app_media.bucket
}
output "hetzner_s3_endpoint_url" {
  description = "Endpoint URL for the S3 bucket for application media files"
  value       = minio_s3_bucket.app_media.bucket_domain_name
}
