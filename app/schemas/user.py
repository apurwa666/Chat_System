from pydantic import BaseModel, EmailStr, field_validator
import re
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

@field_validator("password")
@classmethod
def validate_password(cls, value):
    if len(value)<6:
        raise ValueError("Password must be at least 6 characters long")
    
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")
    
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")
    
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one number")
    
    if not re.search(r"[[!@#$%^&*(),.?\":{}|<>]]"):
        raise ValueError("Password must contain at least one special character")
    
    return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime