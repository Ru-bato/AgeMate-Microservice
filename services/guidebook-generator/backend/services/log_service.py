import logging
from datetime import datetime

from utils.log_parser import parse_log
from repositories.log_repository import LogRepository
from models.log_model import LogModel


class LogService:
    def __init__(self):
        self.repository = LogRepository()

    async def create_log(self, user_id: int, file):
        # 读取文件内容
        content = await file.read()

        # 调用 parse_log 解析文件内容，返回包含 title 和 content 的字典
        parsed_data = parse_log(content.decode("utf-8"))

        # 创建 LogModel 实例，包含 user_id, content, title 和 created_at
        log = LogModel(
            user_id=user_id,
            content=parsed_data["content"],  # 使用解析出的 content
            title=parsed_data["title"],  # 使用解析出的 title
            created_at=datetime.utcnow()
        )

        # 调用插入方法，将 log 存入数据库
        inserted_log = await self.repository.insert_log(log)

        # 将 MongoDB 自动生成的 _id 转换为 log_id
        inserted_log.log_id = str(inserted_log.log_id)  # 将 _id 转换为 log_id

        return inserted_log

    async def get_logs(self, user_id: str):
        return await self.repository.get_logs_by_user(user_id)

    async def delete_log(self, user_id: str, log_id: str):
        await self.repository.delete_log(user_id, log_id)

    async def add_favorite(self, user_id: int, log_id: str):
        return await self.repository.add_favorite(user_id, log_id)

    async def get_favorites(self, user_id: int):
        return await self.repository.get_favorites(user_id)

    async def remove_favorite(self, user_id: int, log_id: str):
        return await self.repository.remove_favorite(user_id, log_id)

    async def search_logs(self, user_id: int, keyword: str):
        # 调用 repository 层，查询符合条件的日志
        return await self.repository.search_logs_by_keyword(user_id, keyword)
