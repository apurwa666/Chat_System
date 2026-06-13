from app.database import Base
from sqlalchemy import Column, Integer, Enum, ForeignKey
import enum

class FriendStatus(str, enum.Enum):
    pending = "pending",
    accepted = "accepted",
    rejected = "rejected"

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index = True)

    requester_id = Column(Integer, ForeignKey("users.id"))
    addressee_id = Column(Integer, ForeignKey("users.id"))

    status = Column(Enum(FriendStatus), default = FriendStatus.pending)