variable "hcloud_token" {
  description = "Hetzner Cloud API Token"
  sensitive   = true
}

variable "hetzner_s3_access_key" {
  description = "Hetzner S3 Access Key"
  sensitive   = true
}

variable "hetzner_s3_secret_key" {
  description = "Hetzner S3 Secret Key"
  sensitive   = true
}

variable "server_location" {
  description = "Location for the server"
  default     = "nbg1"
}

variable "server_type" {
  description = "Hetzner server type"
  default     = "cx32"
}

variable "server_image" {
  description = "Server OS image"
  default     = "ubuntu-22.04"
}

variable "project_name" {
  description = "Name of the project"
}

variable "s3_endpoint_url" {
  description = "Endpoint URL for the S3 Object Storage in Hetzner Cloud"
}

variable "minio_server_url" {
  description = "The url of the Minio S3 objectstorage"
}
