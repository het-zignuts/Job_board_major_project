from app.db.init_db import init_db
from app.api.user import router as user_router
from app.api.company import router as company_router
from app.api.job import router as job_router
from app.api.application import router as application_router
from app.auth.routes import auth_router  
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user_router)
app.include_router(company_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(auth_router)

add_pagination(app)