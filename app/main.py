from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.api.auth import router as auth_router
from app.models import user, message
from app.api.chat import router as chat_router
from app.api.websocket import router as ws_router
from app.api.user import router as user_router

app = FastAPI()

#create tables on startup
Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)
app.include_router(ws_router)
@app.get("/")
def root():
    return {
        "message": "Chat System API"
    }