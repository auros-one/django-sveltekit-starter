variable "project_id" {
  description = "The ID of the project in which resources will be managed."
  type        = string
}

variable "region" {
  description = "The region in which resources will be managed."
  type        = string
  default     = "europe-north1"
}

variable "repo_name" {
  description = "The name of the Artifact Registry repository."
  type        = string
}

variable "repo_description" {
  description = "The description of the Artifact Registry repository."
  type        = string
}

variable "gcp_env_name" {
  description = "The name of the secret in GCP Secret Manager."
  type        = string
}

variable "env_file" {
  description = "The path to the .env.production file."
  type        = string
}

variable "cloud_run_name" {
  description = "The name of the Cloud Run service."
  type        = string
}

variable "image_name" {
  description = "The name of the Docker image."
  type        = string
}
