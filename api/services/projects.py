from bson import ObjectId
from db.models import Project, ProjectCreate
from typing import List
from db.database import db

async def get_all_projects() -> List[Project]:
    """
    Retrieves all projects from the database.
    """
    projects = []
    async for project in db.projects.find():
        projects.append(Project(**project))
    return projects

async def get_project_by_id(project_id: str) -> Project | None:
    """
    Retrieves a project from the database by id.
    """
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if project:
        return Project(**project)

async def create_project(project: ProjectCreate) -> Project:
    """
    Creates a new project in the database.
    """
    project_dict = project.dict()
    result = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": result.inserted_id})
    return Project(**created_project)

async def delete_project(project_id: str) -> Project | None:
    """
    Deletes a project from the database by id.
    """
    project = await db.projects.find_one_and_delete({"_id": ObjectId(project_id)})
    if project:
        return Project(**project)