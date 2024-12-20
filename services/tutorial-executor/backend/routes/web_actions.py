# -*- coding: utf-8 -*-
"""
Web Actions

This module contains the web actions logic for interacting with the frontend and other services.
It includes route definitions, request handling, and response generation for a FastAPI-based application.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Any, Dict, List, Optional
import logging
from models.database import DatabaseUtils  # Assuming this is your MongoDB utility class

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Initialize DatabaseUtils (Assuming you have already set up the MongoDB URI and DB name)
mongo_uri = "mongodb://localhost:27017"  # Replace with your actual MongoDB URI
db_name = "tutorial_executor_db"
db_utils = DatabaseUtils()

class LogEntry(BaseModel):
    """
    Pydantic model for log entries.
    """
    level: str
    message: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("/logs/", response_model=LogEntry)
async def create_log(log_entry: LogEntry):
    """
    Endpoint to create a new log entry.

    Args:
        log_entry (LogEntry): The log entry data.

    Returns:
        LogEntry: The created log entry.
    """
    log_dict = log_entry.dict()
    result = await db_utils.insert_one("logs", log_dict)
    return {**log_dict, "_id": str(result["_id"])}

@router.get("/logs/{log_id}", response_model=LogEntry)
async def read_log(log_id: str):
    """
    Endpoint to read a specific log entry by ID.

    Args:
        log_id (str): The ID of the log entry.

    Returns:
        LogEntry: The requested log entry.
    """
    log = await db_utils.find_one("logs", {"_id": ObjectId(log_id)})
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.get("/logs/", response_model=List[LogEntry])
async def read_logs(
    level: Optional[str] = None,
    message: Optional[str] = None,
    limit: int = 100
):
    """
    Endpoint to read multiple log entries with optional filtering.

    Args:
        level (Optional[str]): Filter logs by level.
        message (Optional[str]): Filter logs by message content.
        limit (int): Limit the number of returned logs. Defaults to 100.

    Returns:
        List[LogEntry]: A list of matching log entries.
    """
    query = {}
    if level:
        query["level"] = level
    if message:
        query["message"] = {"$regex": message, "$options": "i"}

    logs = await db_utils.find_many("logs", query, limit)
    return logs

@router.put("/logs/{log_id}", response_model=LogEntry)
async def update_log(log_id: str, updated_log: LogEntry):
    """
    Endpoint to update a specific log entry by ID.

    Args:
        log_id (str): The ID of the log entry.
        updated_log (LogEntry): The updated log entry data.

    Returns:
        LogEntry: The updated log entry.
    """
    result = await db_utils.update_one("logs", {"_id": ObjectId(log_id)}, updated_log.dict(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Log not found")
    return result

@router.delete("/logs/{log_id}")
async def delete_log(log_id: str):
    """
    Endpoint to delete a specific log entry by ID.

    Args:
        log_id (str): The ID of the log entry.

    Returns:
        dict: Message indicating success or failure.
    """
    deleted = await db_utils.delete_one("logs", {"_id": ObjectId(log_id)})
    if not deleted:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted"}

# Background tasks example
def process_log_background(log_id: str):
    """
    Background task to process a log entry after creation.

    Args:
        log_id (str): The ID of the log entry.
    """
    logging.info(f"Processing log {log_id} in background...")
    # Simulate processing
    import time
    time.sleep(5)  # Simulating long-running task
    logging.info(f"Finished processing log {log_id}")

@router.post("/logs/process/")
async def create_and_process_log(log_entry: LogEntry, background_tasks: BackgroundTasks):
    """
    Endpoint to create a new log entry and process it in the background.

    Args:
        log_entry (LogEntry): The log entry data.
        background_tasks (BackgroundTasks): FastAPI's BackgroundTasks object for running tasks asynchronously.

    Returns:
        LogEntry: The created log entry.
    """
    log_dict = log_entry.dict()
    result = await db_utils.insert_one("logs", log_dict)
    log_id = result["_id"]
    
    # Add background task to process the log
    background_tasks.add_task(process_log_background, log_id)

    return {**log_dict, "_id": log_id}

# Additional endpoints can be added here as needed

# # Error handling middleware can be added here as needed
# @router.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     """
#     Custom exception handler for HTTP exceptions.

#     Args:
#         request (Request): The incoming request.
#         exc (HTTPException): The raised HTTP exception.

#     Returns:
#         JSONResponse: A JSON response containing error details.
#     """
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": str(exc.detail)},
#     )

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Endpoint to check the health status of the service.

    Returns:
        dict: A message indicating the service is healthy.
    """
    return {"message": "Service is healthy"}