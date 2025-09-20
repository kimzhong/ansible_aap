from fastapi import APIRouter, HTTPException
from typing import List
from db.models import Project, ProjectCreate
from services import projects as project_service

router = APIRouter()

@router.get("/projects/", response_model=List[Project])
def read_projects():
    return project_service.get_all_projects()

@router.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int):
    db_project = project_service.get_project_by_id(project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.post("/projects/", response_model=Project)
def create_project(project: ProjectCreate):
    return project_service.create_project(project)

@router.delete("/projects/{project_id}", response_model=Project)
def delete_project(project_id: int):
    db_project = project_service.delete_project(project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project