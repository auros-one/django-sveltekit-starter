
variable "apis_to_enable" {
  description = "List of Google Cloud APIs to enable"
  type        = list(string)
  default     = [
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "storage-component.googleapis.com",
    "servicenetworking.googleapis.com",
    "compute.googleapis.com",
  ]
}

resource "google_project_service" "enable_project_services" {
  for_each = toset(var.apis_to_enable)

  project = var.project_id
  service = each.key

  disable_dependent_services = true
  disable_on_destroy         = false
}
