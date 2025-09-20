from fastapi import FastAPI
from api import tasks, users, projects
from core.config import settings

app = FastAPI(
    title="Ansible AAP API",
    description="A web-based interface to run Ansible playbooks.",
    version="1.0.0",
)

app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(projects.router, prefix=settings.API_V1_STR, tags=["projects"])

@app.get("/")
def read_root():
    """
    Root endpoint of the API.
    """
    return {"message": "Welcome to the Ansible AAP API"}