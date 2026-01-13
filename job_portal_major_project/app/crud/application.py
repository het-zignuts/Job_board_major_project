from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.models.job import Job
from app.crud.job import get_job_by_id
from app.core.enum import ApplicationStatus
import os

def create_application(application: ApplicationCreate, user_id: UUID, job_id: UUID, resume_filename: str, resume_path: str, session: Session) -> ApplicationResponse:
    job=get_job_by_id(job_id, session)
    if not job:
        return None
    application_instance=Application(**application.model_dump())
    application_instance.user_id=user_id
    application_instance.job_id=job_id
    application_instance.resume_filename=resume_filename
    application_instance.resume_path=resume_path
    application_instance.status=ApplicationStatus.APPLIED
    session.add(application_instance)
    session.commit()
    session.refresh(application_instance)
    return ApplicationResponse(id=application_instance.id, user_id=application_instance.user_id, job_id=application_instance.job_id, resume_filename=application_instance.resume_filename, message=application_instance.message, status=application_instance.status, applied_at=application_instance.applied_at, updated_at=application_instance.updated_at)

def get_application_by_id(application_id: UUID, session: Session) -> Optional[ApplicationResponse]:
    application=session.exec(select(Application).where(Application.id==application_id)).first()
    if application:
        return ApplicationResponse(id=application.id, user_id=application.user_id, job_id=application.job_id, resume_filename=application.resume_filename, message=application.message, status=application.status, applied_at=application.applied_at, updated_at=application.updated_at)
    return None

def get_application_by_job_id(job_id: UUID, session: Session) -> list[ApplicationResponse]:
    applications=session.exec(select(Application).where(Application.job_id==job_id)).all()
    return [ApplicationResponse(id=application.id, user_id=application.user_id, job_id=application.job_id, resume_filename=application.resume_filename, message=application.message, status=application.status, applied_at=application.applied_at, updated_at=application.updated_at) for application in applications]

def get_application_by_user_id(user_id: UUID, session: Session) -> list[ApplicationResponse]:
    applications=session.exec(select(Application).where(Application.user_id==user_id)).all()
    return [ApplicationResponse(id=application.id, user_id=application.user_id, job_id=application.job_id, resume_filename=application.resume_filename, message=application.message, status=application.status, applied_at=application.applied_at, updated_at=application.updated_at) for application in applications]

def list_applications(session: Session) -> list[ApplicationResponse]: 
    applications=session.exec(select(Application)).all()
    return [ApplicationResponse(id=application.id, user_id=application.user_id, job_id=application.job_id, resume_filename=application.resume_filename, message=application.message, status=application.status, applied_at=application.applied_at, updated_at=application.updated_at) for application in applications]

def update_application(application_id: UUID, new_application: ApplicationUpdate, session: Session) -> Optional[ApplicationResponse]:
    application=session.exec(select(Application).where(Application.id==application_id)).first()
    if not application:
        return None
    application.status=new_application.status
    application.updated_at=datetime.now(timezone.utc)
    session.add(application)
    session.commit()
    session.refresh(application)
    return ApplicationResponse(id=application.id, user_id=application.user_id, job_id=application.job_id, resume_filename=application.resume_filename, message=application.message, status=application.status, applied_at=application.applied_at, updated_at=application.updated_at)

def delete_application(application_id: UUID, session: Session) -> bool:
    application=session.exec(select(Application).where(Application.id==application_id)).first()
    user_id=application.user_id
    user=session.exec(select(User).where(User.id==user_id)).first()
    resume_path=application.resume_path
    if not application:
        return False
    session.delete(application)
    session.commit()
    if resume_path and os.path.exists(resume_path):
        os.remove(resume_path)
    return True

def add_application_to_job(application_id: UUID, job_id: UUID, session: Session) -> bool:
    application=session.exec(select(Application).where(Application.id==application_id)).first()
    job=session.exec(select(Job).where(Job.id==job_id)).first()
    if not application or not job:
        return False
    if application not in job.applications:
        job.applications.append(application)
    session.add(job)
    session.commit()
    return True

def remove_application_from_job(application: Application, job_id: UUID, session: Session) -> bool:
    # application=session.exec(select(Application).where(Application.id==application_id)).first()
    job=session.exec(select(Job).where(Job.id==job_id)).first()
    if not application or not job:
        return False
    if application in job.applications:
        job.applications.remove(application)
    session.add(job)
    session.commit()
    return True

def add_application_to_user(application_id: UUID, user_id: UUID, session: Session) -> bool:
    application=session.exec(select(Application).where(Application.id==application_id)).first()
    user=session.exec(select(User).where(User.id==user_id)).first()
    if not application or not user:
        return False
    if application not in user.applications:
        user.applications.append(application)
    session.add(user)
    session.commit()
    return True

def remove_application_from_user(application: Application, user_id: UUID, session: Session) -> bool:
    # application=session.exec(select(Application).where(Application.id==application_id)).first()
    user=session.exec(select(User).where(User.id==user_id)).first()
    if not application or not user:
        return False
    if application in user.applications:
        user.applications.remove(application)
    session.add(user)
    session.commit()
    return True
    