import os
import subprocess
import json
import time

global LAGOON_NAME
LAGOON_NAME = os.environ.get("INPUT_LAGOON_NAME", "lagoon")

class LagoonCLIError(Exception):
    pass

def main_process():
    # Read environment variables
    mode = os.environ.get("INPUT_ACTION", "default")
        # Get project and environment names from environment variables
    project_name = os.environ.get("INPUT_LAGOON_PROJECT", "test6-drupal-example-simple")
    environment_name = os.environ.get("INPUT_LAGOON_ENVIRONMENT", "test1copy")
    wait_till_deployed = os.environ.get("INPUT_WAIT_FOR_DEPLOYMENT", "true")

    # Perform actions based on the value of the 'mode' variable
    try:
        if mode == "deploy":
            deploy_environment(project_name, environment_name, wait_till_deployed)
        elif mode == "upsert_variable":
            variable_scope = os.environ.get("INPUT_VARIABLE_SCOPE","runtime")
            variable_name = os.environ.get("INPUT_VARIABLE_NAME", "")
            variable_value = os.environ.get("INPUT_VARIABLE_VALUE", "")
            
            upsert_variable(project_name, environment_name, variable_scope, variable_name, variable_value)
        else:
            default_process()
    except LagoonCLIError as e:
        print(f"Error: {e}")
        exit(1)

def deploy_environment(project_name, environment_name, wait_till_deployed=True):
    
    if not project_name or not environment_name:
        raise LagoonCLIError("Missing project or environment name.")

    print(f"Beginning deployment of {project_name}:{environment_name}")

    # Lagoon CLI command to deploy the latest version with --output-json flag
    lagoon_command = (
        f"/lagoon -l {LAGOON_NAME} --returnData --force --output-json -i ~/.ssh/id_rsa deploy branch "
        f"-p {project_name} -b {environment_name}"
    )

    print(f"Running Lagoon CLI command: {lagoon_command}")  

    # Call the Lagoon CLI command and capture the output
    build_id = run_lagoon_command(lagoon_command)

    print(f"Deployment initiated. Build ID: {build_id}")

    if wait_till_deployed:
        wait_for_deployment(project_name, environment_name, build_id)

    return build_id

def wait_for_deployment(project_name, environment_name, build_id):
    timeout_minutes = 30
    interval_seconds = 60
    start_time = time.time()

    while True:
        # Lagoon CLI command to get deployment status
        status_command = (
            f"/lagoon get deployment --output-json -l {LAGOON_NAME} -p {project_name} -e {environment_name} -N {build_id}"
        )

        # Call the Lagoon CLI command and capture the output
        output = run_lagoon_command(status_command)

        # Process the JSON output and check the status
        if output:
            try:
                status_data = json.loads(output)
                deployment_status = status_data["data"][0]["status"]
                print(f"Deployment Status: {deployment_status}")
            
                # TODO: are there any other terminal states?
                if deployment_status in ["complete"]:
                    return deployment_status
                    break  # Exit the loop if status is complete or failed
                if deployment_status in ["failed", "cancelled"]:
                    raise LagoonCLIError(f"Deployment status: {deployment_status}")
                    break
            # TODO: Should we retry here
            except json.JSONDecodeError as e:
                raise LagoonCLIError(f"Error decoding JSON output: {e}")

        # Check for timeout
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout_minutes * 60:
            raise LagoonCLIError("Timeout reached. Deployment status check aborted.")

        # Wait for the specified interval before checking the status again
        time.sleep(interval_seconds)


def upsert_variable(project_name, environment_name, variable_scope, variable_name, variable_value):

    if variable_scope not in ["global", "build", "runtime", "container_registry", "internal_container_registry"]:
        raise LagoonCLIError("Invalid variable scope. Must be one of: global, build, runtime, container_registry, internal_container_registry")
    
    if variable_name == "":
        raise LagoonCLIError("Variable name cannot be empty.")
    
    if variable_value == "":
        raise LagoonCLIError("Variable value cannot be empty.")

    
    # Lagoon CLI command to deploy the latest version with --output-json flag
    lagoon_command = (
        f"/lagoon -l {LAGOON_NAME} --force --output-json -i ~/.ssh/id_rsa update variable "
        f"-p {project_name} -e {environment_name} -N '{variable_name}' -V '{variable_value}' -S {variable_scope}"
    )

    print(f"Running Lagoon CLI command: {lagoon_command}")  

    # Call the Lagoon CLI command and capture the output
    output = run_lagoon_command(lagoon_command)

    print(f"Variable upsert output: {output}")
    return output


def default_process():
    print("Set an 'action' value of 'deploy' or 'upsert_variable' to use this action.")
    exit(1)
    # Add your code for the default mode here

def run_lagoon_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error executing Lagoon CLI command: {e}")
        print(f"Command output: {e.output.decode('utf-8')}")
        print(f"Command error: {e.stderr.decode('utf-8')}")
        raise LagoonCLIError(f"Error executing Lagoon CLI command: {e}")

if __name__ == "__main__":
    main_process()