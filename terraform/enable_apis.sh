#!/bin/bash

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --project) PROJECT_ID="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if project ID is provided
if [[ -z "$PROJECT_ID" ]]; then
    echo "Project ID is not provided. Use --project to provide it."
    exit 1
fi

# Enable the required APIs
gcloud services enable run.googleapis.com --project $PROJECT_ID
gcloud services enable sqladmin.googleapis.com --project $PROJECT_ID
gcloud services enable secretmanager.googleapis.com --project $PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project $PROJECT_ID
