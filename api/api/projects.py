from fastapi import APIRouter, HTTPException, Depends
from typing import List
from db.models import Project, ProjectCreate
from services import projects as project_service
from core.security import RoleChecker

router = APIRouter()

@router.get("/projects/", response_model=List[Project])
async def read_projects():
    """
    Retrieve all projects.
    """
    return await project_service.get_all_projects()

@router.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: str):
    """
    Retrieve a single project by its ID.
    """
    db_project = await project_service.get_project_by_id(project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.post("/projects/", response_model=Project, dependencies=[Depends(RoleChecker(["admin"]))])
async def create_project(project: ProjectCreate):
    """
    Create a new project.
    Requires admin role.
    """
    return await project_service.create_project(project)

@router.delete("/projects/{project_id}", response_model=Project, dependencies=[Depends(RoleChecker(["admin"]))])
async def delete_project(project_id: str):
    """
    Delete a project by its ID.
    Requires admin role.
    """
    db_project = await project_service.delete_project(project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project