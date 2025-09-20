from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import tempfile
import os
import subprocess
import json
import uuid

app = FastAPI()

# In-memory storage for task results
task_results = {}


def wsl_path(windows_path):
    """Converts a Windows path to a WSL path."""
    path = windows_path.replace('\\', '/')
    drive, rest = path.split(':', 1)
    return f"/mnt/{drive.lower()}{rest}"


def execute_ansible_playbook(task_id: str, playbook_name: str):
    """The actual playbook execution logic."""
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ansible'))
    playbook_path = os.path.join(ansible_dir, f"{playbook_name}.yml")

    if not os.path.exists(playbook_path):
        task_results[task_id] = {"status": "error", "error": f"Playbook {playbook_name}.yml not found"}
        return

    # Convert the ansible directory path to WSL format
    wsl_ansible_dir = wsl_path(ansible_dir)

    # Command to run ansible-runner inside WSL
    command = [
        'wsl',
        'ansible-runner',
        'run',
        wsl_ansible_dir,
        '--playbook',
        f'{playbook_name}.yml',
        '-j'  # Output as JSON
    ]

    try:
        # Run the command
        result = subprocess.run(
            command,
            capture_output=True,
            check=True,
            cwd=ansible_dir  # Run in the ansible directory
        )
        stdout = result.stdout.decode('utf-8', errors='replace')
        # The last line of stdout should be the JSON summary data
        output_lines = stdout.strip().split('\n')
        # Find the JSON output line
        json_output = {}
        for line in reversed(output_lines):
            try:
                # ansible-runner -j prints JSON status on the last line
                parsed_json = json.loads(line)
                json_output = parsed_json
                break
            except json.JSONDecodeError:
                continue

        task_results[task_id] = {"status": "success", "data": json_output}

    except subprocess.CalledProcessError as e:
        error_details = {
            "status": "error",
            "error": e.stderr.decode('utf-8', errors='replace'),
            "stdout": e.stdout.decode('utf-8', errors='replace'),
            "returncode": e.returncode
        }
        task_results[task_id] = error_details
    except FileNotFoundError:
        task_results[task_id] = {
            "status": "error",
            "error": "WSL is not installed or not in the system's PATH."
        }


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/v1/playbooks")
def list_playbooks():
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ansible'))
    playbooks = []
    for filename in os.listdir(ansible_dir):
        if filename.endswith(".yml"):
            playbooks.append(filename.replace(".yml", ""))
    return {"playbooks": playbooks}


@app.post("/api/v1/playbooks/{playbook_name}/run", status_code=202)
def run_playbook(playbook_name: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_results[task_id] = {"status": "running", "data": None}
    background_tasks.add_task(execute_ansible_playbook, task_id, playbook_name)
    return {"task_id": task_id}


@app.get("/api/v1/tasks/{task_id}")
def get_task_result(task_id: str):
    result = task_results.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result