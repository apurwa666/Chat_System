from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.api.auth import router as auth_router

app = FastAPI()

#create tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
@app.get("/")
def root():
    return {
        "message": "Chat System API"
    }