# Run Terraform and output the secrets to a JSON file
terraform apply -auto-approve
terraform output -json > outputs.json

# Extract the necessary secrets
github_actions_sa_key=$(jq -r '.github_actions_sa_key.value' outputs.json)

# Define necessary variables
owner="your-github-username"
repo="your-repo-name"
secret_name="GITHUB_ACTIONS_SA_KEY"

# Get the public key for the repository
response=$(curl -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$owner/$repo/actions/secrets/public-key")

public_key=$(echo $response | jq -r '.key')
key_id=$(echo $response | jq -r '.key_id')

# Encrypt the secret using the public key
encrypted_value=$(echo -n "$github_actions_sa_key" | openssl rsautl -encrypt -pubin -inkey <(echo "$public_key" | base64 --decode) | base64)

# Create or update the secret in the repository
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$owner/$repo/actions/secrets/$secret_name" \
  -d '{"encrypted_value":"'"$encrypted_value"'","key_id":"'"$key_id"'"}'
