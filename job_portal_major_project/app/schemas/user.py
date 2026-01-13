from pydantic import BaseModel, Field   
from typing import Optional
from app.core.enum import UserRole
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    user_name : str
    email : str
    password : str
    role : Optional[UserRole] = Field(default=UserRole.CANDIDATE)
    current_organization : Optional[UUID] = None 

class UserUpdate(BaseModel):
    user_name : str
    email : str
    password : str
    role : UserRole
    current_organization : Optional[UUID] = None 

class UserResponse(BaseModel):
    id : UUID
    user_name : str
    email : str
    role : UserRole
    created_at : datetime
    updated_at : datetime | None
    current_organization : UUID | None