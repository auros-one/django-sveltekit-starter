# Using Terraform Files to Host Django Backends

# 0. Pre-requisites

## System Requirements

-  Terraform
-  Google Cloud SDK

## API Keys

Get API keys for:

- OpenAI
- Helicone
- Sentry

# 1. Create a GCP project

outputs: PROJECT_ID = project-template-396517

# 2. Authenticate to GCP

gcloud auth login
gcloud config set project PROJECT_ID

# 3. Enable Required APIs

```
chmod +x terraform/enable_apis.sh
./terraform/enable_apis.sh --project PROJECT_ID
```

Running the script enables the following APIs in your GCP project:

-   Cloud Run API
-   Cloud SQL Admin API
-   Secret Manager API
-   Artifact Registry API


# 4. Prepare Environment Variables

```
cp .env.production.example .env.production
cp /terraform/variables.tfvars.example /terraform/variables.tfvars
```

Fill out all variables in `.env.production` and `terraform/variables.tfvars`

# 5. Running Terraform

```
cd terraform/
terraform init
terraform plan
```

# 6. Deploying the Django Backend

```
cd terraform/
terraform apply
```


## X. Notes
-   Docs - https://cloud.google.com/docs/terraform/samples
-   Always review the execution plan from the `terraform plan` command before running `terraform apply`.
-   The `terraform apply` command will create resources in your GCP project and may incur costs.
-   You can destroy the resources created by Terraform using the `terraform destroy` command.
