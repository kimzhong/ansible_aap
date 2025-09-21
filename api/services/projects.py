from bson import ObjectId
from db.models import Project, ProjectCreate, ProjectUpdate, ProjectSync
from typing import List, Optional
from db.database import db
from datetime import datetime
import subprocess
import os
import tempfile
import shutil
import logging

logger = logging.getLogger(__name__)

async def get_all_projects() -> List[Project]:
    """
    Retrieves all projects from the database.
    """
    projects = []
    async for project in db.projects.find():
        projects.append(Project(**project))
    return projects

async def get_project_by_id(project_id: str) -> Optional[Project]:
    """
    Retrieves a project from the database by id.
    """
    try:
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        if project:
            return Project(**project)
        return None
    except Exception as e:
        logger.error(f"Error retrieving project {project_id}: {e}")
        return None

async def create_project(project: ProjectCreate) -> Project:
    """
    Creates a new project in the database.
    """
    project_dict = project.dict()
    project_dict["status"] = "active"
    project_dict["created_at"] = datetime.utcnow()
    project_dict["updated_at"] = datetime.utcnow()
    
    result = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": result.inserted_id})
    return Project(**created_project)

async def update_project(project_id: str, project_update: ProjectUpdate) -> Optional[Project]:
    """
    Updates a project in the database.
    """
    try:
        update_data = {k: v for k, v in project_update.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await db.projects.find_one_and_update(
                {"_id": ObjectId(project_id)},
                {"$set": update_data},
                return_document=True
            )
            if result:
                return Project(**result)
        return None
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {e}")
        return None

async def delete_project(project_id: str) -> Optional[Project]:
    """
    Deletes a project from the database by id.
    """
    try:
        project = await db.projects.find_one_and_delete({"_id": ObjectId(project_id)})
        if project:
            # Clean up project directory if it exists
            await _cleanup_project_directory(project_id)
            return Project(**project)
        return None
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {e}")
        return None

async def sync_project(project_id: str) -> ProjectSync:
    """
    Syncs a project with its Git repository.
    """
    try:
        # Update project status to syncing
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"status": "syncing", "updated_at": datetime.utcnow()}}
        )
        
        project = await get_project_by_id(project_id)
        if not project:
            return ProjectSync(
                project_id=project_id,
                status="error",
                message="Project not found"
            )
        
        # Perform Git operations
        sync_result = await _sync_git_repository(project)
        
        # Update project status based on sync result
        new_status = "active" if sync_result["success"] else "error"
        update_data = {
            "status": new_status,
            "updated_at": datetime.utcnow(),
            "last_sync": datetime.utcnow()
        }
        
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_data}
        )
        
        return ProjectSync(
            project_id=project_id,
            status="success" if sync_result["success"] else "error",
            message=sync_result["message"]
        )
        
    except Exception as e:
        logger.error(f"Error syncing project {project_id}: {e}")
        # Update project status to error
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"status": "error", "updated_at": datetime.utcnow()}}
        )
        
        return ProjectSync(
            project_id=project_id,
            status="error",
            message=f"Sync failed: {str(e)}"
        )

async def _sync_git_repository(project: Project) -> dict:
    """
    Performs the actual Git repository synchronization.
    """
    project_dir = f"/tmp/ansible_projects/{project.id}"
    
    try:
        # Create project directory if it doesn't exist
        os.makedirs(project_dir, exist_ok=True)
        
        # Check if it's already a git repository
        if os.path.exists(os.path.join(project_dir, ".git")):
            # Pull latest changes
            result = subprocess.run(
                ["git", "pull", "origin", project.branch],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Repository updated successfully"}
            else:
                return {"success": False, "message": f"Git pull failed: {result.stderr}"}
        else:
            # Clone the repository
            result = subprocess.run(
                ["git", "clone", "-b", project.branch, str(project.git_url), project_dir],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Repository cloned successfully"}
            else:
                return {"success": False, "message": f"Git clone failed: {result.stderr}"}
                
    except subprocess.TimeoutExpired:
        return {"success": False, "message": "Git operation timed out"}
    except Exception as e:
        return {"success": False, "message": f"Git operation failed: {str(e)}"}

async def _cleanup_project_directory(project_id: str):
    """
    Cleans up the project directory when a project is deleted.
    """
    project_dir = f"/tmp/ansible_projects/{project_id}"
    try:
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
            logger.info(f"Cleaned up project directory: {project_dir}")
    except Exception as e:
        logger.error(f"Error cleaning up project directory {project_dir}: {e}")

async def get_project_playbooks(project_id: str) -> List[str]:
    """
    Gets the list of playbooks available in a project.
    """
    try:
        project = await get_project_by_id(project_id)
        if not project:
            return []
        
        project_dir = f"/tmp/ansible_projects/{project_id}"
        if not os.path.exists(project_dir):
            # Try to sync the project first
            sync_result = await sync_project(project_id)
            if sync_result.status == "error":
                return []
        
        # Find all .yml and .yaml files in the project directory
        playbooks = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(('.yml', '.yaml')):
                    # Get relative path from project directory
                    rel_path = os.path.relpath(os.path.join(root, file), project_dir)
                    playbooks.append(rel_path)
        
        return sorted(playbooks)
        
    except Exception as e:
        logger.error(f"Error getting playbooks for project {project_id}: {e}")
        return []