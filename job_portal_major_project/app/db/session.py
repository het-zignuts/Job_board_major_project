from sqlmodel import Session, create_engine
from typing import Generator
from app.core.config import Config

class DatabaseSession:
    def __init__(self, engine):
        self.engine = engine
    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session

engine= create_engine(Config.DATABASE_URL, echo=True)
db_session_manager = DatabaseSession(engine)