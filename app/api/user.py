from fastapi import APIRouter
from app.api.websocket import manager

router = APIRouter(prefix="/users", tags= ["Users"])

@router.get("/online")
def get_online_users():
    return {
        "online_users": manager.get_online_users()
    }