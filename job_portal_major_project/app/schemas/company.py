from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    domain: Optional[str] = None
    company_size: int = Field(default=0)

class CompanyUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    domain: Optional[str] = None
    company_size: int

class CompanyResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    domain: Optional[str] = None
    company_size: int
    owner_id: UUID