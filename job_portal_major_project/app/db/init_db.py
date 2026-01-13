from .session import db_session_manager
from sqlmodel import SQLModel
from app.models.user import User
from app.models.company import Company
from app.models.application import Application
from app.models.job import Job

def init_db():
    SQLModel.metadata.create_all(db_session_manager.engine)