import logging
from datetime import datetime

from utils.log_parser import parse_log
from repositories.log_repository import LogRepository
from models.log_model import LogModel


class LogService:
    def __init__(self):
        self.repository = LogRepository()

    async def create_log(self, user_id: str, file):
        # 异步读取文件内容
        content = await file.read()  # file.read() 改为异步操作
        parsed_content = parse_log(content.decode("utf-8"))

        # 输出解析后的内容到日志
        logging.debug(f"parsed_content={parsed_content}")  # 使用格式化字符串

        # 创建 LogModel 实例
        log = LogModel(user_id=user_id, content=parsed_content, created_at=datetime.utcnow())

        # 插入日志到数据库（假设此方法是异步的）
        return await self.repository.insert_log(log)

    async def get_logs(self, user_id: str):
        return await self.repository.get_logs_by_user(user_id)

    async def delete_log(self, user_id: str, log_id: str):
        await self.repository.delete_log(user_id, log_id)
