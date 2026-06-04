from sqlalchemy.orm import Session
from app.models.message import Message
from sqlalchemy import or_, and_
def create_message(db:Session, sender_id: int, receiver_id: int, content:str):

    message = Message(
        sender_id = sender_id,
        receiver_id = receiver_id,
        content = content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_messages_between_users(db, user1_id:int, user2_id:int):
    return db.query(Message).filter(
        or_(
            and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
            and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
        )
    ).order_by(Message.created_at.asc()).all()