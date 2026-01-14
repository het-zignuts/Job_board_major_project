from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from app.core.enum import UserRole
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Enum as SAEnum
# from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.application import Application

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_name: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: UserRole = Field(sa_column=SAEnum(UserRole, name="userrole", native_enum=True, validate_strings=True, nullable=False    ),default=UserRole.CANDIDATE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    current_organization: Optional[UUID] = Field(default=None, nullable=True, foreign_key="company.id")
    applications: List["Application"] = Relationship(back_populates="user")