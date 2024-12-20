# models/task.py
from typing import Optional, List
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.database import client, db_name

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Task(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    task_id: str
    url: str
    status: str = "pending"
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

async def create_task(task: Task):
    collection = client[db_name]['tasks']
    document = task.dict(by_alias=True)
    result = await collection.insert_one(document)
    task.id = result.inserted_id
    return task

async def get_task(task_id: str):
    collection = client[db_name]['tasks']
    task = await collection.find_one({"_id": ObjectId(task_id)})
    return Task(**task) if task else None

async def update_task(task_id: str, data: dict):
    collection = client[db_name]['tasks']
    await collection.update_one({"_id": ObjectId(task_id)}, {"$set": data})