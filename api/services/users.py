from db.models import User, UserCreate
from core.security import get_password_hash

# This is a mock database. Replace with a real database connection.
fake_users_db = {}

def get_user_by_email(email: str):
    """
    Retrieves a user from the database by email.
    """
    return fake_users_db.get(email)

def create_user(user: UserCreate):
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    fake_users_db[user.email] = db_user
    return db_user

def authenticate_user(email: str, password: str):
    """
    Authenticates a user by email and password.
    """
    user = get_user_by_email(email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user