from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any

class WSMessage(BaseModel):
    type: Literal["init", "message", "typing"]
    payload: Dict[str, Any]