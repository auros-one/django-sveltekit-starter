variable "project_id" {
  description = "The ID of the project in which resources will be managed."
  type        = string
  nullable    = false
}

variable "region" {
  description = "The region in which resources will be managed."
  type        = string
  default     = "europe-north1"
}

variable "project_slug" {
  description = "The slug of the project."
  type        = string
  nullable    = false
}

variable "sentry_dsn" {
  description = "The Sentry DSN for the project"
  type        = string
  default     = ""
}

variable "frontend_domain" {
  description = "The frontend domain for the project"
  type        = string
  nullable    = false
}

variable "placeholder_image" {
  description = "The placeholder image deployed to the Cloud Run service"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "mailgun_api_key" {
  description = "The Mailgun API key for the project"
  type        = string
  nullable    = false
}

variable "mailgun_sender_domain" {
  description = "The Mailgun sender domain for the project"
  type        = string
  nullable    = false
}
