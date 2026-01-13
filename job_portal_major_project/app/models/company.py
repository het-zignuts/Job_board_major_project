from sqlmodel import SQLModel, Field
from typing import Optional, List
from app.core.enum import UserRole
from datetime import datetime
from uuid import UUID, uuid4

class Company(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    website: Optional[str] = Field(default=None, nullable=True)
    location: Optional[str] = Field(default=None, nullable=True)
    domain: Optional[str] = Field(default=None, nullable=True)
    company_size: int = Field(default=0, nullable=False)
    owner_id: UUID = Field(foreign_key="user.id", nullable=False)