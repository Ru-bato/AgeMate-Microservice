from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class LogModel(BaseModel):
    user_id: int
    content: str
    created_at: Optional[datetime] = None
    log_id: Optional[str] = None  # log_id 变为可选字段
    title: str  # 新增标题字段

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # 确保 ObjectId 转换为字符串
        allow_population_by_field_name = True  # 允许通过字段名称访问别名字段
