from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class LogCreate(BaseModel):
    user_id: str
    log_file: bytes

class LogResponse(BaseModel):
    _id: str
    user_id: str
    content: str
    created_at: Optional[datetime] = None