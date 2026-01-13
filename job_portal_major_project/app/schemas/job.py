from ctypes.wintypes import tagSIZE
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.core.enum import EmploymentType, ModeOfWork

class JobCreate(BaseModel):
    title : str 
    description : Optional[str] = None
    location : Optional[str] = None
    mode: ModeOfWork
    employment_type : EmploymentType 
    remuneration_range : Optional[str] = None
    tags: List[str] = []
    # applications: List[str] = []

class JobUpdate(BaseModel):
    title : str 
    description : Optional[str] = None
    location : Optional[str] = None
    mode: ModeOfWork
    employment_type : EmploymentType 
    remuneration_range : Optional[str] = None
    tags: List[str] = []

class JobResponse(BaseModel):
    id : UUID
    title : str 
    description : Optional[str] = None
    location : Optional[str] = None
    mode: ModeOfWork
    employment_type : EmploymentType 
    remuneration_range : Optional[str] = None
    company_id : UUID
    tags: List[str] = []
    posted_at : datetime