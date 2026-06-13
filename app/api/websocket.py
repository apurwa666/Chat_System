from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.connection_manager import ConnectionManager
from jose import jwt, JWTError
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.message_service import create_message
from app.schemas.ws_message import WSMessage
from app.websocket.handlers.message_handler import handle_message
from app.websocket.handlers.init_handler import handle_init

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
            raw_data = await websocket.receive_json()
            msg = WSMessage(**raw_data)

            if msg.type == "init":
                await handle_init(
                    db = db,
                    websocket = websocket,
                    user_id= user_id,
                    payload = msg.payload
                )

            elif msg.type == "message":
                await handle_message(
                    db = db,
                    manager = manager,
                    user_id= user_id,
                    payload= msg.payload
                )

    except WebSocketDisconnect:
        manager.disconnect(user_id)

    finally:
        db.close()
        