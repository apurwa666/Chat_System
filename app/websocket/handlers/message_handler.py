from app.services.message_service import create_message

async def handle_message(db, manager, user_id:int, payload: dict):
    receiver_id = payload[receiver_id]
    content = payload["content"]

    message = create_message(
        db = db,
        sender_id = user_id,
        receiver_id = receiver_id,
        content = content
    )

    await manager.send_message(receiver_id, {
        "type": "message",
        "payload": {
            "id": message.id,
            "sender_id": user_id,
            "content": content
        }
    })