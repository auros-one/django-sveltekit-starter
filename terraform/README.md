# Terraform Deployment Instructions

## 1. Create a GCP Project

Store the project ID and preferred region in an environment variable for later use:

```shell
export PROJECT_ID=test-deployment-5
export GCP_ZONE=europe-north1
```

**note:** don't forget to setup billing for your project

## 2. Authenticate to GCP

```shell
gcloud auth login
gcloud auth application-default login
gcloud config set project $PROJECT_ID
```

## 3. Fill Out terraform Variables

If you're using the django deployment module, you have to fill out it's variables in [`main.tf`](/terraform/main.tf):

```hcl
module "django_deployment" {
  source          = "./modules/django_deployment"
  project_id      = "$PROJECT_ID"
  region          = "$GCP_ZONE"
  project_slug    = "my-project-slug"
  sentry_dsn      = ""
  frontend_domain = ""
}
```

## 3. Create and Reference a GCS Bucket for Terraform State

Terraform keeps track of the state of your infrastructure. We store this state in a GCS bucket so that it can be shared between developers.

Note that the bucket namespace is shared by all users of the system so we choose a globally unique name by using the project ID as a prefix.

```shell
./create_state_bucket.sh
```

It's not possible to use variables in the terraform backend specification so you have to set it manually in the `main.tf` code:

```hcl
terraform {
  backend "gcs" {
    bucket = "$PROJECT_ID-terraform-state"
    prefix = "terraform/state"
  }

  ...

}
```

## 4. Initialize Terraform

```shell
terraform init
```

## 5. Deploy the Infrastructure

```shell
terraform apply
```

## 6. View Outputs

```shell
terraform output
```

## DEBUGGING

-   If there's a `403 permission denied error`, make sure the project ID and other details are correct
