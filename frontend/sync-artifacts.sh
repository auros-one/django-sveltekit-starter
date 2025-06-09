#!/bin/bash

# Sync artifacts from root artifacts folder to frontend static folder
echo "Syncing artifacts from ../artifacts/ to static/artifacts/"

# Create the static artifacts directory if it doesn't exist
mkdir -p static/artifacts

# Copy all markdown files from root artifacts to static artifacts
cp ../artifacts/*.md static/artifacts/

echo "Artifacts synced successfully!"
