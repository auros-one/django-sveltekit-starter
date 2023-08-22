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

-   Always review the execution plan from the `terraform plan` command before running `terraform apply`.
-   The `terraform apply` command will create resources in your GCP project and may incur costs.
-   You can destroy the resources created by Terraform using the `terraform destroy` command.



# Context

I'm trying to deploy the project with terraform, it seems like it has to be done in multiple stages:
1. first resource deployments
- create a service account for django accessing the storages
- create a cloud SQL postgres db
- ... create any other service that can alrlady be created
2. terraform output -> completes required django secrets
- pass the service account credentials to django (paste them into a file?!)
- pass the postgres env vars to django env
- pass the cloud run instance domain name to django env
3. deploy the remaining resources
- cloud run
- store secrets in secret-manager


# Goal: `deploy.py` & `destroy.py`

```shell
> terraform init
terraform init success!
> python deploy.py
deploying initial resources...
running django migrations... (setting up cloud sql tunnel, running manage.py migrate)
deploying django...
deploy success!
initial superuser email: stijn@auros.one
initial superuser password:
creating superuser... (using cloud sql tunnel to run manage.py createsuperuser with the given arguments)
done
```

```shell
> python destroy.py
destroying resources... (basically just calls `terraform destroy`)
```





docker build -t europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image .
docker push europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image


docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -f Dockerfile \
  --cache-from europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image \
  -t europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image \
  .
docker push europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image
gcloud run deploy bbadmin-backend \
  --image=europe-north1-docker.pkg.dev/project-template-396517/project-template-artifact-repo/project-template-backend-image \
  --region=europe-north1 \
  --platform=managed \
  --allow-unauthenticated \
  --add-cloudsql-instances=project-template-396517:europe-north1:project-template-db \
  --env-vars-file=.env.production.yml
