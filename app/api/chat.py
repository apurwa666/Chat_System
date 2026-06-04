from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import create_message
from app.services.message_service import get_messages_between_users
router = APIRouter()

@router.post("/send-message")
def send_message(
    message: MessageCreate,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_message = create_message(
        db=db,
        sender_id = current_user.id,
        receiver_id=message.receiver_id,
        content = message.content
    )

    return {
        "id": new_message.id,
        "sender_id":new_message.sender_id,
        "receiver_id": new_message.receiver_id,
        "content": new_message.content
    }

@router.get("/messages/{user_id}", response_model = list[MessageResponse])
def get_messages(
    user_id:int,
    db:Session = Depends(get_db),
    current_user: User =Depends(get_current_user)
):
    messages = get_messages_between_users(
        db,
        user1_id= current_user.id,
        user2_id= user_id
    )

    return messages