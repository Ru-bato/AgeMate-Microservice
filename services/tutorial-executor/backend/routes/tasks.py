from fastapi import APIRouter, Depends, HTTPException
from models.schemas import TaskRequest, TaskStatus
from services.task_handler import TaskHandler
from typing import List

router = APIRouter()
task_handler = TaskHandler()

@router.post("/tasks/", response_model=str)
async def create_task(request: TaskRequest):
    task_id = await task_handler.create_task(request.dict())
    return task_id

@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    task = await task_handler.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(**task)

@router.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str):
    task = await task_handler.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task_handler.execute_task(task_id, task["model"], task["task"], task["website"])
    return {"message": "Task execution started"}
