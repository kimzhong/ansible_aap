import os
import subprocess
import json

from api.api.tasks import task_results

def wsl_path(windows_path):
    """
    Converts a Windows path to a WSL (Windows Subsystem for Linux) path.
    """
    path = windows_path.replace('\\', '/')
    drive, rest = path.split(':', 1)
    return f"/mnt/{drive.lower()}{rest}"

def execute_ansible_playbook(task_id: str, playbook_name: str):
    """
    Executes an Ansible playbook using ansible-runner inside WSL.
    """
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible'))
    playbook_path = os.path.join(ansible_dir, f"{playbook_name}.yml")

    if not os.path.exists(playbook_path):
        task_results[task_id] = {"status": "error", "error": f"Playbook {playbook_name}.yml not found"}
        return

    wsl_ansible_dir = wsl_path(ansible_dir)

    command = [
        'wsl',
        'ansible-runner',
        'run',
        wsl_ansible_dir,
        '--playbook',
        f'{playbook_name}.yml',
        '-j'
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=True,
            cwd=ansible_dir
        )
        stdout = result.stdout.decode('utf-8', errors='replace')
        output_lines = stdout.strip().split('\n')
        json_output = {}
        for line in reversed(output_lines):
            try:
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