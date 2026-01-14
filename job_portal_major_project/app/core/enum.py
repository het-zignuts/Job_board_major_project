from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    RECRUITER = "RECRUITER"
    CANDIDATE = "CANDIDATE"

class ModeOfWork(str, Enum):
    ONSITE = "ONSITE"
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"

class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    INTERN = "INTERN"

class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"