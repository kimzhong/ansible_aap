from db.models import User, UserCreate, UserInDB
from core.password import get_password_hash, verify_password
from db.database import db
from core.token import decode_access_token

async def get_user_by_email(email: str) -> UserInDB | None:
    user = await db.users.find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

async def get_user_by_token(token: str) -> User | None:
    decoded_token = decode_access_token(token)
    if decoded_token:
        return await db.users.find_one({"email": decoded_token["sub"]})
    return None

async def create_user(user: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(email=user.email, hashed_password=hashed_password)
    await db.users.insert_one(db_user.dict(by_alias=True))
    return db_user

async def authenticate_user(email: str, password: str):
    """
    Authenticates a user by email and password.
    """
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user