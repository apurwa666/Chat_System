from app.models.friendship import Friendship, FriendStatus

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

def are_friends(db, user1_id:int, user2_id:int):
    return db.query(Friendship).filter(
        ((Friendship.requester_id == user1_id) &
         (Friendship.addressee_id == user2_id)) |
        ((Friendship.requester_id == user2_id) &
         (Friendship.addressee_id == user1_id)),
         Friendship.status == "accepted"
    ).first()

def get_incoming_requests(db, user_id: int):
    return db.query(Friendship).filter(
        Friendship.addressee_id == user_id,
        Friendship.status == FriendStatus.pending
    ).all()

def get_outgoing_requests(db, user_id: int):
    return db.query(Friendship).filter(
        Friendship.requester_id == user_id,
        Friendship.status == FriendStatus.pending
    ).all()

def get_friends(db, user_id:int):
    return db.query(Friendship).filter(
        ((Friendship.requester_id == user_id) |
         (Friendship.addressee_id == user_id)),
        Friendship.status == FriendStatus.accepted
    ).all()