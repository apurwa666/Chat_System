from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from app.core.connection_manager import ConnectionManager
from jose import jwt, JWTError
import os
from app.dependencies.db import get_db
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.message_service import create_message


router = APIRouter()
manager = ConnectionManager()
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    
    #authenticate
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            await websocket.close()
            return
        
    except JWTError:
        await websocket.close()
        return
    
    #connect user
    await manager.connect(user_id, websocket)
    db: Session = SessionLocal()
    #listen for messages
    try:
        while True:
            data = await websocket.receive_json()

            receiver_id = data["receiver_id"]
            content = data["content"]

            #1. save to database

            message = create_message(
                db= db,
                sender_id = user_id,
                receiver_id = receiver_id,
                content = content
            )

            #2. await realtime
            await manager.send_message(receiver_id, {
                "id": message.id,
                "sender_id": user_id,
                "content": content
            })

    except WebSocketDisconnect:
        manager.disconnect(user_id)

    finally:
        db.close()
        