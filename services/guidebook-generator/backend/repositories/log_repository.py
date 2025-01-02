from datetime import datetime
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from models.log_model import LogModel
from bson import ObjectId


class LogRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["guidebook_generator"]
        self.collection = self.db["logs"]
        self.favorites_collection = self.db["favorites"]  # 新增收藏表

    async def insert_log(self, log: LogModel):
        # 插入日志
        result = await self.collection.insert_one(log.dict())
        log._id = str(result.inserted_id)  # 将插入后的 ID 转换为字符串
        return log

    async def get_logs_by_user(self, user_id: int):
        logs_cursor = self.collection.find({"user_id": user_id})
        logs = await logs_cursor.to_list(length=100)  # 限制最多返回 100 条

        # 对返回的每个日志记录进行转换，确保 _id 字段被映射到 log_id
        formatted_logs = []
        for log in logs:
            # 将 _id 转换为字符串并将其映射到 log_id 字段
            log["log_id"] = str(log["_id"])  # 将 _id 映射到 log_id
            log.pop("_id", None)  # 删除原始的 _id 字段
            formatted_logs.append(log)

        # 输出 formatted_logs 内容，查看转换后的数据
        print(formatted_logs)

        # 将每个日志条目转换为 LogModel 并返回
        return [LogModel(**log) for log in formatted_logs]

    async def delete_log(self, user_id: int, log_id: str):
        # 删除指定日志
        result = await self.collection.delete_one({"_id": ObjectId(log_id), "user_id": user_id})
        if result.deleted_count == 0:
            raise Exception("Log not found or unauthorized access")

    async def add_favorite(self, user_id: int, log_id: str):
        # 确保日志存在
        log = await self.collection.find_one({"_id": ObjectId(log_id)})
        if not log:
            raise Exception("Log not found")

        # 添加收藏记录
        favorite = {"user_id": user_id, "log_id": log_id}
        existing_favorite = await self.favorites_collection.find_one(favorite)
        if existing_favorite:
            raise Exception("Log is already in favorites")

        await self.favorites_collection.insert_one(favorite)
        return {"message": "Log added to favorites"}

    async def get_favorites(self, user_id: int) -> List[LogModel]:
        # 获取用户收藏的日志
        favorites_cursor = self.favorites_collection.find({"user_id": user_id})
        favorites = await favorites_cursor.to_list(length=100)

        # 获取收藏日志的 log_id 列表，log_id 已经是字符串类型，不需要转换为 ObjectId
        log_ids = [ObjectId(fav["log_id"]) for fav in favorites]

        # 获取收藏日志的详细信息，直接使用 log_id 字符串查询
        logs_cursor = self.collection.find({"_id": {"$in": log_ids}})
        logs = await logs_cursor.to_list(length=100)

        # 将日志数据映射到 LogModel 对象，注意处理 _id 字段到 log_id 字段的映射
        formatted_logs = []
        for log in logs:
            log["log_id"] = str(log["_id"])  # 将 _id 转换为 log_id
            log.pop("_id", None)  # 删除原始的 _id 字段
            formatted_logs.append(log)

        # 将每个日志条目转换为 LogModel 并返回
        return [LogModel(**log) for log in formatted_logs]

    async def remove_favorite(self, user_id: int, log_id: str):
        # 取消收藏
        result = await self.favorites_collection.delete_one({"user_id": user_id, "log_id": log_id})
        if result.deleted_count == 0:
            raise Exception("Favorite not found or unauthorized access")
        return {"message": "Log removed from favorites"}

    async def search_logs_by_keyword(self, user_id: int, keyword: str):
        # 使用正则表达式在 title 字段中匹配关键字
        logs_cursor = self.collection.find({
            "user_id": user_id,
            "title": {"$regex": keyword, "$options": "i"}  # 不区分大小写
        })
        logs = await logs_cursor.to_list(length=100)  # 最多返回 100 条

        # 格式化日志数据，返回 LogModel 实例
        formatted_logs = []
        for log in logs:
            log["log_id"] = str(log["_id"])  # 将 _id 映射到 log_id 字段
            log.pop("_id", None)  # 删除原始的 _id 字段
            formatted_logs.append(log)

        return [LogModel(**log) for log in formatted_logs]