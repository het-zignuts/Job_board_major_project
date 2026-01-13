from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlmodel import Session
from uuid import UUID
import os
import shutil
from app.db.session import db_session_manager
from app.auth.deps import get_current_user
from app.models.user import User
from app.core.enum import UserRole
from app.schemas.application import ApplicationResponse
from app.crud.application import *
from app.crud.job import get_job_by_id
from app.crud.company import get_company_by_id
from app.core.config import Config

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application_api(
    job_id: UUID,
    message: str = "",
    resume: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(db_session_manager.get_session),
):
    job = get_job_by_id(job_id, session)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    company = get_company_by_id(job.company_id, session)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    uploads_dir = Config.UPLOAD_RESUME_DIR
    os.makedirs(uploads_dir, exist_ok=True)
    resume_filename = f"{current_user.id}_{job_id}_{resume.filename}"
    resume_path = os.path.join(uploads_dir, resume_filename)
    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    application_data = ApplicationCreate(message=message)
    application = create_application(application_data, current_user.id, job_id, resume_filename, resume_path, session)
    if not application:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create application")
    added_to_job= add_application_to_job(application.id, job_id, session)
    if not added_to_job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to link application to job")
    added_to_user= add_application_to_user(application.id, current_user.id, session)
    if not added_to_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to link application to user")
    return application

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application_api(application_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    application = get_application_by_id(application_id, session)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if application.user_id != current_user.id and current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return application

@router.get("/jobs/{job_id}", response_model=list[ApplicationResponse])
def get_applications_by_job_api(job_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    job = get_job_by_id(job_id, session)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can view applications for this job")
    applications = get_application_by_job_id(job_id, session)
    return applications

@router.get("/users/{user_id}", response_model=list[ApplicationResponse])
def get_applications_by_user_api(user_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    applications = get_application_by_user_id(user_id, session)
    return applications

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application_status_api(application_id: UUID, new_status: ApplicationStatus, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can update application status")
    application = get_application_by_id(application_id, session)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    job = get_job_by_id(application.job_id, session)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    updated_application = update_application(application_id, ApplicationUpdate(status=new_status), session)
    if not updated_application:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update application")
    return updated_application

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application_api(application_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    application = get_application_by_id(application_id, session)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if application.user_id != current_user.id and current_user.role != UserRole.ADMIN and current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    removed_from_job= remove_application_from_job(application, application.job_id, session)
    removed_from_user=remove_application_from_user(application, application.user_id, session)
    if not removed_from_job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to unlink application from job")
    if not removed_from_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to unlink application from user")
    success = delete_application(application_id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete application")
    return

