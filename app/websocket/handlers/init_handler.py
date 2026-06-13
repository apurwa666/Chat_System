from app.services.message_service import get_messages_between_users


async def handle_init(db, websocket, user_id: int, payload: dict):
    receiver_id = payload["receiver_id"]

    messages = get_messages_between_users(db, user_id, receiver_id)

    await websocket.send_json({
        "type": "history",
        "payload": [
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "receiver_id": m.receiver_id,
                "content": m.content,
                "created_at": str(m.created_at)
            }
            for m in messages
        ]
    })