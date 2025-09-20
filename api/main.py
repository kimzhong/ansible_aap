from fastapi import FastAPI
from api import tasks, users
from core.config import settings
from db.database import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])

@app.get("/")
def read_root():
    """
    Root endpoint of the API.
    """
    return {"message": "Welcome to the Ansible AAP API"}