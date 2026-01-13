from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.core.enum import ApplicationStatus

class ApplicationCreate(BaseModel):
    message: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    resume_filename: str
    message: Optional[str] = None
    status: ApplicationStatus
    applied_at: datetime
    updated_at: Optional[datetime] = None