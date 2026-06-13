from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.services.user_service import get_user_by_username
from app.services.friend_service import send_friend_request, accept_friend_request, get_incoming_requests, get_outgoing_requests, get_friends
from app.core.security import get_current_user

router = APIRouter(prefix = "/friends", tags = ["Friends"])

@router.post("/request/{username}")
def request_friend(username:str, db: Session = Depends(get_db), current_user = Depends(get_db)):

    target_user = get_user_by_username(db, username)

    if not target_user:
        raise HTTPException(status_code=404, detail = "User Not Found")
    
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail = "Cannot add yourself")
    
    return send_friend_request(db, current_user.id, target_user.id)

@router.post("/accept/{request_id}")
def accept_request(request_id: int, db: Session = Depends(get_db)):
    return accept_friend_request(db, request_id)

@router.get("/incoming")
def incoming(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_incoming_requests(db, current_user.id)

@router.get("/outgoing")
def outgoing(db:Session = Depends(get_db), current_user= Depends(get_current_user)):
    return get_outgoing_requests(db, current_user.id)

@router.get("/")
def friends(db:Session  = Depends(get_db), current_user = Depends(get_current_user)):
    return get_friends(db, current_user.id)