from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

def get_database() -> AsyncIOMotorClient:
    return db.client

def connect_to_mongo():
    """
    Connects to the MongoDB database.
    """
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)

def close_mongo_connection():
    """
    Closes the MongoDB connection.
    """
    db.client.close()