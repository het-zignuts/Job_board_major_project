from passlib.context import CryptContext
from app.core.config import Config
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from enum import Enum
from uuid import uuid4, UUID
from app.models.refreshtoken import RefreshToken
from sqlmodel import Session
from fastapi import HTTPException
from app.models.user import User
from sqlmodel import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(email: str, plain_password: str, session: Session) -> bool:
        user=session.exec(select(User).where(User.email==email)).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return pwd_context.verify(plain_password, user.password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        payload = data.copy()
        expires_at=payload.get('iat') + int(Config.TOKEN_EXPIRY_TIME) * 60
        # expire = datetime.utcfromtimestamp(expires_at)
        # expire = datetime.utcnow() + timedelta(minutes=60)
        # iat=datetime.utcnow()
        # payload.update({"iat": int(iat.timestamp())})
        print("Token issued at (iat):", int(payload.get('iat')))
        payload.update({"exp": int(expires_at)})
        print("Token expiration time (exp):", int(expires_at))
        payload.update({"type": "access"})
        encoded_jwt = jwt.encode(payload, Config.SECRET_KEY, Config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def create_refresh_token(user_id: UUID, role: str):
        created_at=datetime.now(timezone.utc)
        exp_time=created_at + timedelta(days=20)
        token_id=str(uuid4())
        payload={
            "sub": user_id,
            "token_id": token_id,
            "created_at": int(created_at.timestamp()),
            "exp": int(exp_time.timestamp()),
            "type": "refresh",
            "role": role
        }
        encoded_refresh_jwt=jwt.encode(payload, Config.REFRESH_SECRET_KEY, Config.ALGORITHM)
        return {
            "ref_token": encoded_refresh_jwt,
            "token_id": token_id,
            "created_at": created_at,
            "exp": exp_time
            }

    @staticmethod
    def store_refresh_token(token_id: str, exp_time: datetime, user_id: UUID, session: Session):
        token=RefreshToken(token_id=token_id, exp=exp_time, user_id=user_id)
        session.add(token)
        session.commit()
        session.refresh(token)