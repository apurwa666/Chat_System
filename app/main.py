from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.api.auth import router as auth_router
from app.models import user, message
from app.api.chat import router as chat_router

app = FastAPI()

#create tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)
@app.get("/")
def root():
    return {
        "message": "Chat System API"
    }