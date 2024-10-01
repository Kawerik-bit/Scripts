import requests
import subprocess
import json
import sys
import time

# Git settings
GITHUB_TOKEN = "github_token_here" 
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "your_repo_owner_user_or_organization" 
REPO_NAME = "repo_name"  

# Headers for GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def trigger_workflow(branch):
    """
    Trigger the GitHub Actions workflow for the given branch.
    """
    workflow_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/build.yml/dispatches"
    
    payload = {
        "ref": branch
    }

    response = requests.post(workflow_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 204:
        print(f"Workflow triggered successfully for branch: {branch}")
    else:
        print(f"Failed to trigger workflow: {response.content}")

def deploy_to_environment(environment, tag=None):
    """
    Deploy to a specific environment (e.g., stage, production) based on branch/tag.
    """
    deploy_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/deployments"
    
    payload = {
        "ref": tag if tag else "main",
        "environment": environment,
        "auto_merge": False,
        "required_contexts": []  # skips status checks for deployment
    }

    response = requests.post(deploy_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print(f"Deployment started to {environment} environment.")
    else:
        print(f"Failed to deploy to {environment}: {response.content}")

def rollback_deployment(deployment_id):
    """
    Roll back a deployment if errors are detected.
    """
    deployment_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/deployments/{deployment_id}/statuses"

    payload = {
        "state": "failure"
    }

    response = requests.post(deployment_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print(f"Rollback successful for deployment {deployment_id}.")
    else:
        print(f"Failed to rollback deployment: {response.content}")

def get_latest_deployment_status(environment):
    """
    Get the status of the latest deployment to a specific environment.
    """
    deployments_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/deployments"
    
    params = {
        "environment": environment,
        "per_page": 1
    }

    response = requests.get(deployments_url, headers=headers, params=params)
    
    if response.status_code == 200:
        deployment = response.json()[0]
        deployment_id = deployment['id']
        statuses_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/deployments/{deployment_id}/statuses"
        statuses_response = requests.get(statuses_url, headers=headers)
        
        if statuses_response.status_code == 200:
            statuses = statuses_response.json()
            return statuses[0]['state']  # Return the current status
        else:
            print(f"Failed to get deployment statuses: {statuses_response.content}")
    else:
        print(f"Failed to get deployments: {response.content}")
    return None

def monitor_deployment(environment, timeout=600):
    """
    Monitor the deployment status and handle rollback if it fails.
    """
    start_time = time.time()

    while True:
        status = get_latest_deployment_status(environment)
        if status == "success":
            print(f"Deployment to {environment} was successful.")
            break
        elif status == "failure":
            print(f"Deployment to {environment} failed. Rolling back...")
            rollback_deployment(environment)
            break
        elif time.time() - start_time > timeout:
            print(f"Deployment to {environment} timed out. Rolling back...")
            rollback_deployment(environment)
            break

        print(f"Monitoring deployment... Status: {status}")
        time.sleep(30)  # 30 second check

def main():
    """
    Main CI/CD pipeline automation function.
    """
    # Arguments to handle options like branch/tag and environment
    if len(sys.argv) != 3:
        print("Usage: python pipeline_automation.py <branch|tag> <environment>")
        sys.exit(1)

    ref = sys.argv[1]
    environment = sys.argv[2]

    if environment not in ["stage", "production"]:
        print("Invalid environment. Choose either 'stage' or 'production'.")
        sys.exit(1)

    # Workflow trigger for branch or tag
    trigger_workflow(ref)

    # Deploy to specified environment
    deploy_to_environment(environment, tag=ref if ref.startswith("v") else None)

    # Monitor deployment status and handle rollback if necessary
    monitor_deployment(environment)

if __name__ == "__main__":
    main()

# Script to streamline a continuous integration and continuous deployment process in github
# Replace variables in begining with desired repos/users etc...
# Run examples: with "python pipeline_automation.py main stage" - from main branch to stage deploy
# "python pipeline_automation.py $v0.1 production" - deploy from tag v0.1 to production ( replace the $v0.1 variable with your tag)
