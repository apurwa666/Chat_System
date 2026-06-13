from app.models.friendship import Friendship

def send_friend_request(db, requester_id:int, addressee_id:int):
    request = Friendship(
        requester_id = requester_id,
        addressee_id = addressee_id,
        status = "pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def accept_friend_request(db, request_id:int):
    request = db.query(Friendship).filter(Friendship.id==request_id).first()

    if request:
        request.status = "accepted"
        db.commit()
    
    return request