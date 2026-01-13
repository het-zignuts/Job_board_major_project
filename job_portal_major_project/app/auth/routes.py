from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import db_session_manager
from app.crud.user import *
from app.auth.deps import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import AccessToken, RefreshToken
from app.core.security import Security
from app.core.config import Config
from jose import jwt, JWTError
from app.models.refreshtoken import RefreshToken as RefreshTokenModel
# from datetime import datetime
from app.core.config import Config
import time
from uuid import UUID

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(db_session_manager.get_session)):
    user= create_user(session, user)
    if not user:
        raise HTTPException(status_code=400, detail="User already registered...")
    return user

@auth_router.post("/login", response_model=AccessToken)
def login_user(user: UserCreate, session: Session = Depends(db_session_manager.get_session)):
    if Security.verify_password(user.email, user.password, session):
        user_db=get_user_by_email(session, user.email)
        if not user_db:
            raise HTTPException(status_code=400, detail="User not found, please register")
        access_token = Security.create_access_token({"sub": str(user_db.id), "role": user_db.role, "iat": time.time()})
        print("LOGIN TOKEN ISSUED AT:", int(time.time()))
        refresh_jwt_token = Security.create_refresh_token(str(user_db.id), user_db.role)
        Security.store_refresh_token(token_id=refresh_jwt_token["token_id"], exp_time=refresh_jwt_token["exp"], user_id=user_db.id, session=session)
        refresh_token=refresh_jwt_token["ref_token"]
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")

@auth_router.post("/refresh", response_model=AccessToken)
def refresh_access_token(refresh_token: RefreshToken, session: Session = Depends(db_session_manager.get_session)):
    token_data = jwt.decode(refresh_token.refresh_token, Config.REFRESH_SECRET_KEY, algorithms=[Config.ALGORITHM])
    if not token_data or token_data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    ref_token_db= session.exec(select(RefreshTokenModel).where(RefreshTokenModel.token_id == token_data["token_id"])).first()
    if not ref_token_db:
        raise HTTPException(status_code=401, detail="Refresh token not found or revoked")
    new_access_token = Security.create_access_token({"sub": token_data["sub"], "role": token_data["role"], "iat": time.time()})
    new_refresh_jwt_token = Security.create_refresh_token(token_data["sub"], token_data["role"])
    Security.store_refresh_token(token_id=new_refresh_jwt_token["token_id"], exp_time=new_refresh_jwt_token["exp"], user_id=UUID(token_data["sub"]), session=session)
    session.delete(ref_token_db)
    session.commit()
    return {"access_token": new_access_token, "refresh_token": new_refresh_jwt_token["ref_token"], "token_type": "bearer"}