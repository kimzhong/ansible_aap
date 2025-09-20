from fastapi import APIRouter, HTTPException, BackgroundTasks
import os
import uuid

from services.ansible_runner import execute_ansible_playbook
from store import task_results
from schemas.task import RunPlaybookRequest

router = APIRouter()

@router.get("/playbooks")
def list_playbooks():
    """
    Lists all available Ansible playbooks by scanning the 'ansible' directory.
    """
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible'))
    playbooks = []
    for filename in os.listdir(ansible_dir):
        if filename.endswith(".yml"):
            playbooks.append(filename.replace(".yml", ""))
    return {"playbooks": playbooks}

@router.post("/playbooks/{playbook_name}/run", status_code=202)
def run_playbook(playbook_name: str, request: RunPlaybookRequest, background_tasks: BackgroundTasks):
    """
    Triggers the execution of a specific Ansible playbook in the background.
    A unique task ID is generated to track the execution status.
    """
    task_id = str(uuid.uuid4())
    task_results[task_id] = {"status": "running", "data": None}
    background_tasks.add_task(
        execute_ansible_playbook, 
        task_id, 
        playbook_name, 
        inventory=request.inventory, 
        extra_vars=request.extra_vars
    )
    return {"task_id": task_id}

@router.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    """
    Retrieves the current status and result of a previously triggered playbook execution task.
    """
    result = task_results.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result