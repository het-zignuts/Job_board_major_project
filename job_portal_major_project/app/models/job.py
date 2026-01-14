from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Column, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from app.core.enum import ModeOfWork, EmploymentType
# from sqlalchemy.orm import Mapped, relationship
# from app.models.application import Application

if TYPE_CHECKING:
    from app.models.application import Application

class Job(SQLModel, table=True):
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title : str = Field(index=True, nullable=False)
    description : Optional[str] = Field(default=None, nullable=True)
    location : Optional[str] = Field(default=None, nullable=True)
    mode: ModeOfWork = Field(sa_column=SAEnum(ModeOfWork, name="modeofwork", native_enum=True, validate_strings=True, nullable=False),default=ModeOfWork.ONSITE)
    employment_type : EmploymentType = Field(sa_column=SAEnum(EmploymentType, name="employmenttype", native_enum=True, validate_strings=True, nullable=False),default=EmploymentType.FULL_TIME)
    remuneration_range : Optional[str] = Field(default=None, nullable=True)
    company_id : UUID = Field(foreign_key="company.id", nullable=False)
    tags: List[str] = Field(sa_column=Column(JSONB, nullable=True), default_factory=list)
    posted_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc), nullable=False)
    applications: List["Application"] = Relationship(back_populates="job")