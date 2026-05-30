from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(db, user)

        return {
            "id": created_user.id,
            "username": created_user.username,
            "email" : created_user.email
        }
    except Exception as e:
        raise HTTPException(status_code = 400, detail =  str(e))
    
@router.get("/users", response_model = list[UserResponse])
def list_users(db:Session = Depends(get_db)):
    return get_users(db)