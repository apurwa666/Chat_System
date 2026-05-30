from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["argon2"], deprecated = "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(db:Session, user: UserCreate):

    #check existing emails
    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        raise ValueError("Email already registered")
    
    existing_username = db.query(User).filter(User.username == user.username).first()

    #check existing usernames
    if existing_username:
        raise ValueError("Username already taken")

    hashed_password = hash_password(user.password)

    #create user object
    db_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password
    )


    #save to DB
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db:Session):
    return db.query(User).all()