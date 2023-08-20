variable "project_id" {
  description = "The ID of the project in which resources will be managed."
  type        = string
}

variable "region" {
  description = "The region in which resources will be managed."
  type        = string
  default     = "europe-north1"
}

variable "project_slug" {
  description = "The slug of the project."
  type        = string
}

variable "env_file" {
  description = "The path to the .env.production file."
  type        = string
}

variable "image_name" {
  description = "The name of the Docker image."
  type        = string
}

variable "username" {
  description = "The username for the database."
  type        = string
}

variable "password" {
  description = "The password for the database."
  type        = string
}
