from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base model for a user.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str

class User(UserBase):
    """
    Model for representing a user in the database.
    """
    hashed_password: str

    class Config:
        orm_mode = True