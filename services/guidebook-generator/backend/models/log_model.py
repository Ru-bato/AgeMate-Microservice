from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class LogModel(BaseModel):
    _id: Optional[str]
    user_id: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

