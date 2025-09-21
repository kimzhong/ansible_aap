from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db.models import Project, ProjectCreate, ProjectUpdate, ProjectSync
from services import projects as project_service
from core.security import RoleChecker

router = APIRouter()

@router.get("/", response_model=List[Project])
async def get_projects():
    """
    Get all projects.
    """
    return await project_service.get_all_projects()

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """
    Get a project by ID.
    """
    project = await project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.post("/", response_model=Project)
async def create_project(
    project: ProjectCreate,
    _: bool = Depends(RoleChecker(["admin"]))
):
    """
    Create a new project. Requires admin role.
    """
    try:
        return await project_service.create_project(project)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create project: {str(e)}"
        )

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    _: bool = Depends(RoleChecker(["admin"]))
):
    """
    Update a project. Requires admin role.
    """
    project = await project_service.update_project(project_id, project_update)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.delete("/{project_id}", response_model=Project)
async def delete_project(
    project_id: str,
    _: bool = Depends(RoleChecker(["admin"]))
):
    """
    Delete a project. Requires admin role.
    """
    project = await project_service.delete_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.post("/{project_id}/sync", response_model=ProjectSync)
async def sync_project(
    project_id: str,
    _: bool = Depends(RoleChecker(["admin", "user"]))
):
    """
    Sync a project with its Git repository.
    """
    try:
        return await project_service.sync_project(project_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync project: {str(e)}"
        )

@router.get("/{project_id}/playbooks", response_model=List[str])
async def get_project_playbooks(project_id: str):
    """
    Get all playbooks available in a project.
    """
    project = await project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        return await project_service.get_project_playbooks(project_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get project playbooks: {str(e)}"
        )