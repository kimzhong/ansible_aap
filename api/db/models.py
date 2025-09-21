from typing import Any
from pydantic import BaseModel, EmailStr, Field, GetCoreSchemaHandler, HttpUrl
from pydantic_core import core_schema
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(
                                cls.validate
                            ),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class UserBase(BaseModel):
    """
    Base model for a user.
    """
    email: EmailStr
    roles: List[str] = []

class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str

class UserUpdate(BaseModel):
    """
    Model for updating a user.
    """
    email: EmailStr | None = None
    roles: List[str] | None = None
    password: str | None = None

class User(UserBase):
    """
    Model for representing a user in the database.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserInDB(User):
    hashed_password: str

class ProjectBase(BaseModel):
    """
    Base model for a project.
    """
    name: str
    description: Optional[str] = None
    git_url: HttpUrl
    branch: str = "main"

class ProjectCreate(ProjectBase):
    """
    Model for creating a new project.
    """
    pass

class ProjectUpdate(BaseModel):
    """
    Model for updating a project.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    git_url: Optional[HttpUrl] = None
    branch: Optional[str] = None

class Project(ProjectBase):
    """
    Model for representing a project in the database.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: str = "active"  # active, syncing, error
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_sync: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class ProjectSync(BaseModel):
    """
    Model for project sync response.
    """
    project_id: str
    status: str
    message: str
    sync_started_at: datetime = Field(default_factory=datetime.utcnow)