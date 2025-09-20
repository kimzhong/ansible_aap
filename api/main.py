from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import tempfile
import os
import subprocess
import json
import uuid

# Initialize FastAPI application
app = FastAPI()

# In-memory storage for task results.
# This is a simple dictionary to store the status and results of Ansible playbook executions.
# In a production environment, you might want to use a more persistent storage like a database.
task_results = {}


def wsl_path(windows_path):
    """
    Converts a Windows path to a WSL (Windows Subsystem for Linux) path.
    This is necessary because the Ansible runner is executed within WSL.
    Example: 'D:\ansible_aap\ansible' becomes '/mnt/d/ansible_aap/ansible'
    """
    path = windows_path.replace('\\', '/')
    drive, rest = path.split(':', 1)
    return f"/mnt/{drive.lower()}{rest}"


def execute_ansible_playbook(task_id: str, playbook_name: str):
    """
    Executes an Ansible playbook using ansible-runner inside WSL.
    This function is run in the background.

    Args:
        task_id: The unique ID for this task execution.
        playbook_name: The name of the playbook to execute (without the .yml extension).
    """
    # Get the absolute path to the 'ansible' directory
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ansible'))
    playbook_path = os.path.join(ansible_dir, f"{playbook_name}.yml")

    # Check if the playbook file exists
    if not os.path.exists(playbook_path):
        task_results[task_id] = {"status": "error", "error": f"Playbook {playbook_name}.yml not found"}
        return

    # Convert the ansible directory path to WSL format for the ansible-runner command
    wsl_ansible_dir = wsl_path(ansible_dir)

    # Construct the command to run ansible-runner inside WSL
    command = [
        'wsl',
        'ansible-runner',
        'run',
        wsl_ansible_dir,
        '--playbook',
        f'{playbook_name}.yml',
        '-j'  # Output the final status as a JSON object
    ]

    try:
        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            check=True, # Raise an exception for non-zero exit codes
            cwd=ansible_dir  # Set the working directory
        )
        stdout = result.stdout.decode('utf-8', errors='replace')
        
        # The last line of stdout from ansible-runner with '-j' is the JSON summary.
        output_lines = stdout.strip().split('\n')
        json_output = {}
        # Iterate backwards to find the first valid JSON line, which is the summary
        for line in reversed(output_lines):
            try:
                parsed_json = json.loads(line)
                json_output = parsed_json
                break
            except json.JSONDecodeError:
                # Ignore lines that are not valid JSON
                continue

        # Store the successful result
        task_results[task_id] = {"status": "success", "data": json_output}

    except subprocess.CalledProcessError as e:
        # Handle errors during playbook execution
        error_details = {
            "status": "error",
            "error": e.stderr.decode('utf-8', errors='replace'),
            "stdout": e.stdout.decode('utf-8', errors='replace'),
            "returncode": e.returncode
        }
        task_results[task_id] = error_details
    except FileNotFoundError:
        # Handle case where WSL is not installed or not in PATH
        task_results[task_id] = {
            "status": "error",
            "error": "WSL is not installed or not in the system's PATH."
        }


@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"Hello": "World"}


@app.get("/api/v1/playbooks")
def list_playbooks():
    """
    Lists all available Ansible playbooks in the 'ansible' directory.
    It finds all files ending with .yml and returns their names without the extension.
    """
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ansible'))
    playbooks = []
    for filename in os.listdir(ansible_dir):
        if filename.endswith(".yml"):
            playbooks.append(filename.replace(".yml", ""))
    return {"playbooks": playbooks}


@app.post("/api/v1/playbooks/{playbook_name}/run", status_code=202)
def run_playbook(playbook_name: str, background_tasks: BackgroundTasks):
    """
    Triggers the execution of a specific Ansible playbook in the background.

    Args:
        playbook_name: The name of the playbook to run.
        background_tasks: FastAPI's background tasks manager.

    Returns:
        A task ID that can be used to poll for the result.
    """
    task_id = str(uuid.uuid4())
    # Immediately set the status to 'running'
    task_results[task_id] = {"status": "running", "data": None}
    # Add the playbook execution to the background tasks
    background_tasks.add_task(execute_ansible_playbook, task_id, playbook_name)
    return {"task_id": task_id}


@app.get("/api/v1/tasks/{task_id}")
def get_task_result(task_id: str):
    """
    Retrieves the status and result of a playbook execution task.

    Args:
        task_id: The ID of the task to retrieve.

    Returns:
        The task's status and data, or a 404 error if the task is not found.
    """
    result = task_results.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result