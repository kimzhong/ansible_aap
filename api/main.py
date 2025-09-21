from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tasks, users, projects
from core.config import settings

app = FastAPI(
    title="Ansible AAP API",
    description="A web-based interface to run Ansible playbooks.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])

@app.get("/")
def read_root():
    """
    Root endpoint of the API.
    """
    return {"message": "Welcome to the Ansible AAP API"}