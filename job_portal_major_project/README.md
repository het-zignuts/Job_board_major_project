# JOB BOARD - A robust backend Platform for job seekers and recruiters
## Tech-Stack:
- Python (3.14.2)
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- JWT (JSON Web Tokens)
- Pytest
- BaseHTTPMiddleware

## Users:
- Admin
- Candidates
- Recruiters

## Key Features:

### Authentication & Authorization
- User registration and login
- JWT‑based authentication (Access & Refresh tokens)
- Role‑based access control:
    - Candidate
    - Recruiter
    - Admin

### User Management
- Create and manage users
- Role assignment 
- User‑specific permissions

### Company Management
- Recruiters can create and manage company profiles
- Companies linked to recruiters
- Admin override permissions

### Job Management
Recruiters can:
- Create jobs
- Update jobs
- Delete jobs
Candidates can:
- List jobs
- Search (by title and job description) and filter jobs (based on location, work-mode, employment type, tags, etc.)
- Job Filters
They get well paginated & sorted responses (by time posted at).

### Job Applications
Candidates can apply to jobs
- Resume upload support
- File system storage for resumes
- Status display and update reflection (applied, under_review, accepted, rejected)

## Project Structure:
```text
job_portal_major_project
├── app/
│   ├── api/ .................... (API endppoints defined here)
│   │   ├── application.py
│   │   ├── company.py 
│   │   ├── job.py 
│   │   └── user.py 
│   ├── auth/ .................... (Dependencies and authentication routes (registration, login, token refresh))
│   │   ├── deps.py 
│   │   └── routes.py
│   ├── core/ .................... (Core settings)
│   │   ├── config.py  (gives env variables)
│   │   ├── security.py (gives token management and password security utils)
│   │   └── enum.py (enum classes)
│   ├── crud/ ..................... (Business Logic (CRUD operations))
│   │   ├── application.py 
│   │   ├── job.py 
│   │   ├── company.py 
│   │   └── user.py
│   ├── models/ ................... (database models (SQLModel))
│   │   ├── application.py 
│   │   ├── job.py 
│   │   ├── company.py 
│   │   ├── refreshtoken.py 
│   │   └── user.py
│   ├── schema/ .....................(Pydantic Schemas)
│   │   ├── application.py 
│   │   ├── job.py 
│   │   ├── company.py 
│   │   ├── token.py 
│   │   └── user.py
│   ├── db/
│   │   ├── session.py ..............(Session Management)
│   │   └── init_db.py ..............(Database Initializaton)
│   ├── tests/ ......................(Unit tests)
│   │   ├── conftest.py 
│   │   ├── factory.py 
│   │   ├── test_application.py 
│   │   ├── test_job.py 
│   │   ├── test_company.py 
│   │   ├── test_token.py 
│   │   └── test_user.py
│   └── main.py  ....................(Entry Point)
├── requirements.txt 
└── README.md
```

## Project and Environment Setup:

- Project Requirements:
```text
- Python (3.14.x)
- uvicorn 
- FastAPI
- SQLModel
- Pydantic
- PostgreSQL
- JWT
```

- Environment Setup:

1. Create a new env in project folder `job_portal_major_project`:
```bash
python -m venv .venv
```

2. Activate the environemnt:
```bash
source .venv/bin/activate
```

3. Intsall the dependencies:
```bash
pip install -r requirements.txt
```

4. Running the server:
```bash
uvicorn app.main:app --reload
```
The server starts running on (https://127.0.0.1:8000)

#### Interactive docs:
- Swagger UI → https://127.0.0.1:8000/docs
- ReDoc → https://127.0.0.1:8000/redoc

## Database Setup (Persistent Database: PostgreSQL):

```psql
CREATE USER job_portal_user WITH PASSWORD 'password';
CREATE DATABASE job_portal OWNER job_portal_user;
GRANT ALL PRIVILEGES ON DATABASE job_portal TO job_portal_user;
```
#### For tests, a separate test database is used and reset automatically.

## Running Tests
```python
pytest
```
#### Features of test setup:
- Test database isolation
- Schema reset per session
- Temporary file system for resume uploads
- Role‑based test fixtures (used factory fixtures)

### API Summary:

#### Job APIs:

| **Request Pattern** | **Method** | **Operation**         | **Remarks**                   | **Path Operation**            |
| ------------------- | ---------- | --------------------- | ----------------------------- | ----------------------------- |
| `/jobs/`            | POST       | Create a new job      | Recruiter only                | `create_job_api(...)`         |
| `/jobs/`            | GET        | List all jobs         | Supports filters & pagination | `list_jobs_api(...)`          |
| `/jobs/{job_id}`    | GET        | Retrieve job by ID    | Public                        | `get_job_api(...)`            |
| `/jobs/{job_id}`    | PUT        | Update/Replace job    | Recruiter (owner) only        | `update_job_api(...)`         |
| `/jobs/{job_id}`    | DELETE     | Delete job            | Recruiter (owner) / Admin     | `delete_job_api(...)`         |

#### Application APIs:

| **Request Pattern**                 | **Method** | **Operation**                    | **Remarks**                   | **Path Operation**                   |
| ----------------------------------- | ---------- | -------------------------------- | ----------------------------- | ------------------------------------ |
| `/applications/jobs/{job_id}/apply` | POST       | Apply for a job                  | Candidate only, resume upload | `create_application_api(...)`        |
| `/applications/{application_id}`    | GET        | Get application by ID            | Owner / Recruiter             | `get_application_api(...)`           |
| `/applications/user/me`             | GET        | List current user’s applications | Candidate only                | `list_my_applications_api(...)`      |
| `/applications/job/{job_id}`        | GET        | List applications for a job      | Recruiter (job owner)         | `list_job_applications_api(...)`     |
| `/applications/{application_id}`    | PUT        | Update application status        | Recruiter only                | `update_application_status_api(...)` |
| `/applications/{application_id}`    | DELETE     | Delete application               | Owner / Recruiter / Admin     | `delete_application_api(...)`        |

#### User APIs:

| **Request Pattern** | **Method** | **Operation**              | **Remarks**   | **Path Operation**             |
| ------------------- | ---------- | -------------------------- | ------------- | ------------------------------ |
| `/users/`         | POST        | Create a user | All users  | `create_user_api(...)`    |
| `/users/me`  | GET        | Get user by ID             | Admin only    | `get_user_by_id_api(...)`      |
| `/users/me`  | PUT        | Update user profile        | Owner / Admin | `update_user_api(...)`         |
| `/users/me`  | DELETE     | Delete user account        | Admin only    | `delete_user_api(...)`         |
| `/users/`           | GET        | List all users             | Admin only    | `list_users_api(...)`          |

#### Company APIs:

| **Request Pattern**       | **Method** | **Operation**          | **Remarks**           | **Path Operation**                |
| ------------------------- | ---------- | ---------------------- | --------------------- | --------------------------------- |
| `/companies/`             | POST       | Create a company       | Recruiter only        | `create_company_api(...)`         |
| `/companies/`             | GET        | List all companies     | Public                | `list_companies_api(...)`         |
| `/companies/{company_id}` | GET        | Get company by ID      | Public                | `get_company_api(...)`            |
| `/companies/{company_id}` | PUT        | Update company details | Company owner / Admin | `update_company_api(...)`         |
| `/companies/{company_id}` | DELETE     | Delete company         | Admin only            | `delete_company_api(...)`         |

#### Authentication APIs:

| **Request Pattern** | **Method** | **Operation**    | **Remarks**                   |
| ------------------- | ---------- | ---------------- | ----------------------------- |
| `/auth/register`    | POST       | Register user    | Candidate / Recruiter         |
| `/auth/login`       | POST       | Login user       | Returns JWT                   |
| `/auth/me`          | GET        | Get current user | Requires Authorization header |


#### You can check the API endpoints and test them using Swagger UI at (https://127.0.0.1:8000/docs) while running the app.



## Check out the docs for FastAPI [here](https://fastapi.tiangolo.com/).
### Author:  
#### Het Shukla