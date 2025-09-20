from fastapi import FastAPI
from api.api import tasks

app = FastAPI()

app.include_router(tasks.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}