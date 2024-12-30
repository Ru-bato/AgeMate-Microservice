import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.log_service import LogService
from schemas.log_schema import LogCreate, LogResponse
from typing import List

log_router = APIRouter(prefix="/logs", tags=["logs"])
log_service = LogService()

@log_router.post("/", response_model=LogResponse)
async def upload_log(file: UploadFile = File(...), user_id: int = 1):
    # 允许的文件类型
    allowed_types = ["text/plain", "application/octet-stream"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only text files are allowed")

    return await log_service.create_log(user_id, file)

@log_router.get("/", response_model=List[LogResponse])
async def get_logs(user_id: int):
    return await log_service.get_logs(user_id)

@log_router.delete("/{log_id}")
async def delete_log(log_id: str, user_id: int):
    await log_service.delete_log(user_id, log_id)
    return {"message": "Log deleted successfully"}

@log_router.post("/favorites/")
async def add_favorite(user_id: int, log_id: str):
    return await log_service.add_favorite(user_id, log_id)

@log_router.get("/favorites/")
async def get_favorites(user_id: int):
    return await log_service.get_favorites(user_id)

@log_router.delete("/favorites/")
async def remove_favorite(user_id: int, log_id: str):
    return await log_service.remove_favorite(user_id, log_id)

@log_router.get("/search", response_model=List[LogResponse])
async def search_logs(user_id: int, keyword: str):
    logs = await log_service.search_logs(user_id, keyword)
    return logs



