from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from uuid import UUID
from fastapi_pagination import Page, paginate
from app.db.session import db_session_manager
from app.auth.deps import get_current_user
from app.models.user import User
from app.core.enum import UserRole
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.crud.job import *
from app.crud.company import *

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_api(job: JobCreate, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can create job postings")
    company = get_company_by_id(current_user.current_organization, session)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    created_job = create_job(job, company.id, session)
    return created_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job_api(job_id: UUID, session: Session = Depends(db_session_manager.get_session)):
    job = get_job_by_id(job_id, session)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.get("/", response_model=Page[JobResponse])
def list_jobs_api(
    session: Session = Depends(db_session_manager.get_session),
    search_query: Optional[str] = Query(None),
    location: Optional[str] = None,
    mode: Optional[ModeOfWork] = None,
    employment_type: Optional[EmploymentType] = None,
    tags: Optional[list[str]] = Query(None),
    order_by: str = "posted_at",
    order_type : str = "desc",
):
    jobs = list_jobs(
        session,
        search_query=search_query,
        location=location,
        mode=mode,
        employment_type=employment_type,
        tags=tags,
        order_by=order_by,
        order_type=order_type,
    )
    return paginate(jobs)

@router.put("/{job_id}", response_model=JobResponse)
def update_job_api(job_id: UUID, job: JobUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can update job postings")
    current_job = get_job_by_id(job_id, session)
    if not current_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    company = get_company_by_id(current_user.current_organization, session)
    if not company or current_job.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions to update this job")
    updated_job = update_job(job_id, job, session)
    return updated_job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_api(job_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can delete job postings")
    current_job = get_job_by_id(job_id, session)
    if not current_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    company = get_company_by_id(current_user.current_organization, session)
    if not company or current_job.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions to delete this job")
    success = delete_job(job_id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return