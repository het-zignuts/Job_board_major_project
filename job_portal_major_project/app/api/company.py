from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from app.db.session import db_session_manager
from app.auth.deps import get_current_user
from app.models.user import User
from app.core.enum import UserRole
from app.schemas.company import *
from app.crud.company import *

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company_api(company: CompanyCreate, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role not in ("candidate", "recruiter", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to create company")
    created_company = create_company(company, current_user.id, session)
    if created_company is None:
        raise HTTPException(
            status_code=400,
            detail="Company already exists"
        )
    return created_company


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_api(company_id: UUID, session: Session = Depends(db_session_manager.get_session)):
    company = get_company_by_id(company_id, session)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company_api(company_id: UUID, company: CompanyUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    updated_company = update_company(company_id, company, session)
    if not updated_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return updated_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company_api(company_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    success = delete_company(company_id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return

@router.get("/", response_model=list[CompanyResponse])
def list_companies_api(session: Session = Depends(db_session_manager.get_session)):
    companies = list_companies(session)
    return companies
