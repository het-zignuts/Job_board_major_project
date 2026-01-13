from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import Config
from app.core.security import Security
from uuid import UUID
from app.models.user import User
from app.core.enum import UserRole
from app.db.session import db_session_manager
from sqlmodel import Session
import time
from datetime import datetime, timezone
from app.crud.user import *

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
auth_header_scheme = HTTPBearer()

def get_current_user(session : Session = Depends(db_session_manager.get_session), creds: HTTPAuthorizationCredentials = Depends(auth_header_scheme)) -> User:
    try:
        print("Inside get_current_user... getting creds")
        token=creds.credentials
        print("Token received: " + token)
        print("Now (time.time):", time.time())
        print("Now (utc):", datetime.now(timezone.utc).timestamp())
        print("Token exp:", payload_exp := jwt.get_unverified_claims(token)["exp"])
        print("Diff (exp - now):", payload_exp - time.time())
        payload = jwt.decode(token, Config.SECRET_KEY,algorithms=[Config.ALGORITHM])
        print("Payload decoded: " + str(payload))
        if payload:
            print("Payload exists...")
            user_id: UUID = UUID(payload.get("sub"))
            tkn_type: str|None=payload.get("type")
            if user_id is None or tkn_type is None:
                print("user id:" + str(user_id)+" this one..")
                if tkn_type != "access": print("token type:" + tkn_type)
                if user_id is None: print("user id is none")
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            # user= session.get(User, user_id)
            user=get_user_model_instance(user_id, session)
            if not user:
                raise HTTPException(status_code=401, detail="User not found...")
            return user
        else:
            raise HTTPException(status_code=401, detail="Authentication failed...")
    except JWTError as e:
        print("JWT Error occurred...")
        print("JWT ERROR TYPE:", type(e))
        print("JWT ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def is_admin(current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True

def is_candidate(current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True

def is_recruiter(current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True

# def check_owner_or_admin(user_id: UUID, current_user: User) -> bool:
#     if current_user.role == UserRole.ADMIN or current_user.id == user_id:
#         return True
#     raise HTTPException(status_code=403, detail="Insufficient permissions")

# def check_recipe_owner_or_admin(recipe: Recipe, user:User)->bool:
#     try:
#         print("Checking recipe owner or admin...")
#         print("Recipe owner id:", recipe.uploaded_by)
#         print("User id:", user.id)
#         print("User role:", user.role)
#         if user.role == UserRole.ADMIN or recipe.uploaded_by == user.id:
#             return True
#     except Exception as e:
#         print("Exception in check_recipe_owner_or_admin:", e)
#         print("user id and role :", user.id, user.role)
#         print("recipe owner id :", recipe.uploaded_by)
#         raise HTTPException(status_code=403, detail="Insufficient permissions")
        
  