from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class LogCreate(BaseModel):
    user_id: int
    log_file: bytes


class LogResponse(BaseModel):
    log_id: str
    user_id: int
    content: str
    created_at: Optional[datetime] = None
    title: str  # 返回时也包括 title 字段