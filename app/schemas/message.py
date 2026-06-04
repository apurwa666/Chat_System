from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    id:int
    sender_id:int
    receiver_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)