from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import db_session_manager
from app.auth.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.crud.user import *
from app.core.enum import UserRole

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_api(current_user: User = Depends(get_current_user), session: Session=Depends(db_session_manager.get_session)):
    user= get_user_by_id(current_user.id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/me", response_model=UserResponse)
def update_current_user_api(user: UserUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    updated_user = update_user(current_user.id, user, session)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_api(current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    success = delete_user(current_user.id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return   

@router.get("/", response_model=list[UserResponse])
def list_all_users_api(current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    users = list_users(session)
    return users