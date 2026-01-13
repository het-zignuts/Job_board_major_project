import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")

# Load .env ONLY for local / tests
if ENV != "production":
    load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

    UPLOAD_RESUME_DIR = os.getenv("UPLOAD_RESUME_DIR", "uploads/resumes")

    TOKEN_EXPIRY_TIME = int(os.getenv("TOKEN_EXPIRY_TIME", "30"))  # minutes
    REFRESH_TOKEN_EXPIRY_TIME = int(os.getenv("REFRESH_TOKEN_EXPIRY_TIME", "20"))  # days
    ALGORITHM = os.getenv("ALGORITHM", "HS256")


#  Validate required env vars (fail fast)
if ENV == "production":
    required = [
        "SECRET_KEY",
        "REFRESH_SECRET_KEY",
        "DATABASE_URL",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")


#  Fix Render Postgres URL driver
if Config.DATABASE_URL and Config.DATABASE_URL.startswith("postgresql://"):
    Config.DATABASE_URL = Config.DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1,
    )
