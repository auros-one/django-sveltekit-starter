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
  default     = "../.env.production"
}

variable "db_password" {
  description = "The password for the database."
  type        = string
}
