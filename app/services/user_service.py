from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def create_user(db:Session, user: UserCreate):

    #check existing emails
    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        raise ValueError("Email already registered")
    
    existing_username = db.query(User).filter(User.username == user.username).first()

    #check existing usernames
    if existing_username:
        raise ValueError("Username already taken")

   

    #create user object
    db_user = User(
        username = user.username,
        email = user.email,
        password = hash_password(user.password)
    )


    #save to DB
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db:Session):
    return db.query(User).all()

def get_user_by_username(db, username:str):
    return db.query(User).filter(User.username == username).first()