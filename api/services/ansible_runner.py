import os
import subprocess
import json
from typing import Dict, Any

from store import task_results

"""
This module provides functions for running Ansible playbooks.
"""
def wsl_path(windows_path: str) -> str:
    """
    Converts a Windows path to a WSL path.

    Args:
        windows_path: The Windows path to convert.

    Returns:
        The WSL path.
    """
    path = windows_path.replace('\\', '/')
    drive, rest = path.split(':', 1)
    return f"/mnt/{drive.lower()}{rest}"

async def execute_ansible_playbook(playbook_name: str, inventory: str, extra_vars: dict) -> dict:
    """
    Executes an Ansible playbook using ansible-runner in WSL.

    Args:
        playbook_name: The name of the playbook to execute.
        inventory: The inventory to use for the playbook.
        extra_vars: Extra variables to pass to the playbook.

    Returns:
        A dictionary containing the task result.
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
    ]

    inventory_path = None
    if inventory:
        inventory_path = os.path.join(ansible_dir, f"inventory_{task_id}.ini")
        with open(inventory_path, "w") as f:
            f.write(inventory)
        command.extend(['--inventory', wsl_path(inventory_path)])

    if extra_vars:
        command.extend(['--extravars', json.dumps(extra_vars)])
    
    command.append('-j')


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
    finally:
        if inventory_path and os.path.exists(inventory_path):
            os.remove(inventory_path)