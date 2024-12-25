from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ActionRecord(BaseModel):
    timestamp: datetime
    userID: int # 假设有用户id作为user表主键
    selected_option: str
    action_type: str
    action_value: Optional[str]
    task_id: str  # 用于关联特定任务
    step_number: int  # 步骤序号
    execution_time: float  # API 调用耗时

class MongoDBHandler:
    def __init__(self, mongodb_url: str):
        from motor.motor_asyncio import AsyncIOMotorClient
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client.tutorial_executor
        self.collection = self.db.action_records

    async def save_action(self, 
                         userID: int,
                         selected_option: str, 
                         action: str, 
                         value: str, 
                         task_id: str,
                         step_number: int,
                         execution_time: float):
        record = ActionRecord(
            timestamp=datetime.datetime.now(),
            userID=userID,
            selected_option=selected_option,
            action_type=action,
            action_value=value,
            task_id=task_id,
            step_number=step_number,
            execution_time=execution_time
        )
        
        await self.collection.insert_one(record.dict()) 