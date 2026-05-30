from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.dependencies import get_current_user

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
    

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    #1. Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    #2. Verify Password
    if not verify_password(password, user.password):
        raise HTTPException(status_code = 401, detail = "Invalid Credentials")
    
    #3. create token
    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

#get all users
@router.get("/users", response_model = list[UserResponse])
def list_users(db:Session = Depends(get_db)):
    return get_users(db)

#get the current logged in user
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }