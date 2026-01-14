from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.core.enum import ApplicationStatus
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.user import User

class Application(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    job_id: UUID = Field(foreign_key="job.id", nullable=False)
    job: Optional["Job"] = Relationship(back_populates="applications")
    resume_filename: str = Field(nullable=False)
    resume_path: str = Field(nullable=False)
    message : Optional[str] = Field(default=None, nullable=True)
    status: ApplicationStatus = Field(sa_column=SAEnum(ApplicationStatus, name="applicationstatus", native_enum=True, validate_strings=True, nullable=False), default=ApplicationStatus.APPLIED)
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    user: Optional["User"] = Relationship(back_populates="applications")