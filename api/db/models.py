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


class ProjectBase(BaseModel):
    """
    Base model for a project.
    """
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    """
    Model for creating a new project.
    """
    pass

class Project(ProjectBase):
    """
    Model for representing a project in the database.
    """
    id: int

    class Config:
        orm_mode = True