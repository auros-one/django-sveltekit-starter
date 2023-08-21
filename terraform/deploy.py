import os
import subprocess


def run_command(command):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}\n{stderr.decode()}")
        return None
    return stdout.decode()


def main():
    # Do some sanity checks:
    # - check if the project is already deployed -> check if f"{project_slug}" exists or is available
    # - check if .env.production exists, only variables that are set in this file are allowed to be empty

    # Enable the required APIs
    # TODO: is this ok or should we do this in python
    print("Enabling required APIs...")
    project_id = run_command("terraform output -raw project_id")
    run_command(f"./enable_apis.sh --project {project_id}")

    # First stage: Deploy initial resources
    print("Deploying initial resources...")
    run_command("terraform apply -auto-approve")

    # Second stage: Update Django settings
    print("Updating Django settings...")

    # Fetch outputs from Terraform
    # db_host = run_command("terraform output -raw sql_instance_connection_name")
    service_account_key = run_command("terraform output -raw backend_gcs_key")

    # Save the service account key to a JSON file
    # TODO: is this the best way to do this?
    # TODO: -> isn't it possible to just give the cloud run resource the service account key or access?
    with open("service_account.json", "w") as f:
        f.write(service_account_key)
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

    # Update secrets
    # TODO:
    #  1. store the generated env vars in .env.production
    #  2. upload the env to the Secret Manager

    # Create tunnel to Cloud SQL
    # ...

    # Run Django migrations
    print("Running Django migrations...")
    run_command("python manage.py migrate")

    # Third stage: Deploy remaining resources (Cloud Run)
    print("Deploying Django...")
    run_command("terraform apply -auto-approve")

    # Create a Django superuser
    print("Creating Django superuser...")
    superuser_email = input("Superuser email: ")
    superuser_password = input("Superuser password: ")
    run_command(
        f"python manage.py createsuperuser --email {superuser_email} --password {superuser_password} --noinput"
    )
    print(
        f"Superuser created. Email: {superuser_email}\nIt's recommended to change the password via the Django Admin."
    )

    print("Done!")
    print(
        "You can now access the Django Admin via the following URL:"
    )  # TODO: make it print the cloud run url + /admin

    print("To set up Github Actions, add the following secrets to your repository:")
    # TODO: print the required secrets


if __name__ == "__main__":
    main()
