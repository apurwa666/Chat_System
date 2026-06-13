from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.user import User
from sqlalchemy import or_, and_, desc
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

def get_messages_between_users(db, user1_id:int, user2_id:int, limit:int = None):
    query = db.query(Message).filter(
        or_(
            and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
            and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
        )
    ).order_by(Message.created_at.asc())

    if limit:
        query = query.limit(limit)

    return query.all()

def get_chat_list(db, user_id:int):
    #get all users who ever chatted with the current user
    messages = db.query(Message).filter(
        (Message.sender_id == user_id)|
        (Message.receiver_id == user_id)
    ).order_by(Message.created_at.desc()).all()

    seen = set()
    chat_list = []

    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id

        if other_user_id in seen:
            continue

        seen.add(other_user_id)

        other_user = db.query(User).filter(User.id==other_user_id).first()

        chat_list.append({
            "user_id": other_user.id,
            "username": other_user.username,
            "last_message": msg.content,
            "timestamp": msg.created_at
        })

        return chat_list
