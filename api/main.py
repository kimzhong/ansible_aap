from fastapi import FastAPI
from api.api import tasks, users
from core.config import settings

app = FastAPI()

app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])

@app.get("/")
def read_root():
    """
    Root endpoint of the API.
    """
    return {"message": "Welcome to the Ansible AAP API"}