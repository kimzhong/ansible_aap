from db.models import Project, ProjectCreate
from typing import List

# This is a mock database. Replace with a real database connection.
fake_projects_db = {}
next_project_id = 1

def get_all_projects() -> List[Project]:
    """
    Retrieves all projects from the database.
    """
    return list(fake_projects_db.values())

def get_project_by_id(project_id: int) -> Project | None:
    """
    Retrieves a project from the database by id.
    """
    return fake_projects_db.get(project_id)

def create_project(project: ProjectCreate) -> Project:
    """
    Creates a new project in the database.
    """
    global next_project_id
    db_project = Project(id=next_project_id, **project.dict())
    fake_projects_db[next_project_id] = db_project
    next_project_id += 1
    return db_project

def delete_project(project_id: int) -> Project | None:
    """
    Deletes a project from the database by id.
    """
    return fake_projects_db.pop(project_id, None)