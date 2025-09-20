from fastapi import APIRouter, HTTPException, BackgroundTasks
import os
import uuid

from services.ansible_runner import execute_ansible_playbook

router = APIRouter()

# In-memory storage for task results.
task_results = {}

@router.get("/playbooks")
def list_playbooks():
    """
    Lists all available Ansible playbooks.
    """
    ansible_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible'))
    playbooks = []
    for filename in os.listdir(ansible_dir):
        if filename.endswith(".yml"):
            playbooks.append(filename.replace(".yml", ""))
    return {"playbooks": playbooks}

@router.post("/playbooks/{playbook_name}/run", status_code=202)
def run_playbook(playbook_name: str, background_tasks: BackgroundTasks):
    """
    Triggers the execution of a specific Ansible playbook.
    """
    task_id = str(uuid.uuid4())
    task_results[task_id] = {"status": "running", "data": None}
    background_tasks.add_task(execute_ansible_playbook, task_id, playbook_name)
    return {"task_id": task_id}

@router.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    """
    Retrieves the status and result of a playbook execution task.
    """
    result = task_results.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result