from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import or_
from app.models.job import Job
from app.models.application import Application
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.core.enum import ModeOfWork, EmploymentType

def create_job(job: JobCreate, company_id: UUID, session: Session) -> JobResponse:
    job_instance=Job(**job.model_dump())
    job_instance.company_id=company_id
    job_instance.applications=[]
    session.add(job_instance)
    session.commit()
    session.refresh(job_instance)
    return JobResponse(id=job_instance.id, title=job_instance.title, description=job_instance.description, location=job_instance.location, mode=job_instance.mode, employment_type=job_instance.employment_type, remuneration_range=job_instance.remuneration_range, company_id=job_instance.company_id, tags=job_instance.tags, posted_at=job_instance.posted_at)

def get_job_by_id(job_id: UUID, session: Session) -> Optional[JobResponse]:
    job=session.exec(select(Job).where(Job.id==job_id)).first()
    if job:
        return JobResponse(id=job.id, title=job.title, description=job.description, location=job.location, mode=job.mode, employment_type=job.employment_type, remuneration_range=job.remuneration_range, company_id=job.company_id, tags=job.tags, posted_at=job.posted_at)
    return None

def list_jobs(session: Session, 
              search_query: Optional[str] = None,
              location: Optional[str] = None,
              mode: Optional[ModeOfWork] = None,
              employment_type: Optional[EmploymentType] = None,
              tags: Optional[list[str]] = None,
              order_by: str = "posted_at",  
              order_type : str = "desc",
              ) -> list[JobResponse]: 
    query = select(Job)
    if search_query:
        query = query.where(or_(Job.title.ilike(f"%{search_query}%"), Job.description.ilike(f"%{search_query}%")))
    if location:
        query = query.where(Job.location == location)
    if mode:
        query = query.where(Job.mode == mode)
    if employment_type:
        query = query.where(Job.employment_type == employment_type)
    if tags:
        query = query.where(Job.tags.contains(tags))
    if order_by == "posted_at":
        if order_type == "asc":
            query = query.order_by(Job.posted_at.asc())
        else:
            query = query.order_by(Job.posted_at.desc())
    jobs=session.exec(query).all()
    return [JobResponse(id=job.id, title=job.title, description=job.description, location=job.location, mode=job.mode, employment_type=job.employment_type, remuneration_range=job.remuneration_range, company_id=job.company_id, tags=job.tags, posted_at=job.posted_at) for job in jobs]

def update_job(job_id: UUID, new_job: JobUpdate, session: Session) -> Optional[JobResponse]:
    job=session.exec(select(Job).where(Job.id==job_id)).first()
    if not job:
        return None
    job_data = new_job.model_dump()
    for key, value in job_data.items():
        setattr(job, key, value)
    session.add(job)
    session.commit()
    session.refresh(job)
    return JobResponse(id=job.id, title=job.title, description=job.description, location=job.location, mode=job.mode, employment_type=job.employment_type, remuneration_range=job.remuneration_range, company_id=job.company_id, tags=job.tags, posted_at=job.posted_at)

def delete_job(job_id: UUID, session: Session) -> bool:
    job=session.exec(select(Job).where(Job.id==job_id)).first()
    applications=session.exec(select(Application).where(Application.job_id == job_id)).all()
    for application in applications:
        session.delete(application)
    if not job:
        return False
    session.delete(job)
    session.commit()
    return True