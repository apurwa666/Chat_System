async def handle_typing(manager, user_id: int, payload: dict):
    receiver_id = payload["receiver_id"]
    is_typing = payload["is_typing"]

    await manager.send_message(receiver_id,{
        "type": "typing",
        "payload": {
            "sender_id": user_id,
            "is_typing": is_typing
        }
    })