#!/bin/bash

# Check if PROJECT_ID is set
if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: PROJECT_ID environment variable is not set."
    echo "Please set the PROJECT_ID environment variable with the GCP project ID."
    exit 1
fi

# Check if GCP_ZONE is set
if [ -z "$GCP_ZONE" ]; then
    echo "ERROR: GCP_ZONE environment variable is not set."
    echo "Please set the GCP_ZONE environment variable with your preferred GCP zone (e.g. us-east4)."
    exit 1
fi

# Create the GCS bucket for Terraform state
BUCKET_NAME="${PROJECT_ID}-terraform-state"
echo "Creating the GCS bucket for Terraform state: $BUCKET_NAME..."
if gcloud storage buckets create "gs://${BUCKET_NAME}" --location=$GCP_ZONE --project="$PROJECT_ID"; then
    echo "Bucket created successfully: $BUCKET_NAME"
else
    echo "ERROR: Failed to create bucket. Please check the error message above."
    exit 1
fi

# Reminder to set the bucket name in main.tf
echo -e "\n!!! Update your main.tf with the following backend configuration: !!!"
echo -e "\nterraform {"
echo "  backend \"gcs\" {"
echo "    bucket = \"$BUCKET_NAME\""
echo "    prefix = \"terraform/state\""
echo "  }"
echo -e "\n...\n"
echo "}"
echo -e "\nReplace the existing backend block with the one above."
