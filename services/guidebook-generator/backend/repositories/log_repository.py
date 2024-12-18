from motor.motor_asyncio import AsyncIOMotorClient
from models.log_model import LogModel
from bson import ObjectId


class LogRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["log_database"]
        self.collection = self.db["logs"]

    async def insert_log(self, log: LogModel):
        # 插入日志
        result = await self.collection.insert_one(log.dict())
        log._id = str(result.inserted_id)  # 将插入后的 ID 转换为字符串
        return log

    async def get_logs_by_user(self, user_id: str):
        # 查询指定用户的日志
        logs_cursor = self.collection.find({"user_id": user_id})
        logs = await logs_cursor.to_list(length=100)  # 限制最多返回 100 条
        return [LogModel(**log) for log in logs]

    async def delete_log(self, user_id: str, log_id: str):
        # 删除指定日志
        result = await self.collection.delete_one({"_id": ObjectId(log_id), "user_id": user_id})
        if result.deleted_count == 0:
            raise Exception("Log not found or unauthorized access")
