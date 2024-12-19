# -*- coding: utf-8 -*-
"""
CRUD Operations

This module contains functions to perform CRUD (Create, Read, Update, Delete) operations on the database.
It uses Motor for asynchronous MongoDB interactions.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from typing import List, Optional, Dict, Any
from .schemas import LogEntry, Configuration, LargeModelResponse, Screenshot, User, PyObjectId
import pymongo

# Initialize MongoDB client
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client.mydatabase  # Replace 'mydatabase' with your actual database name


# Log Entry CRUD Operations
async def create_log_entry(log_entry: LogEntry):
    """
    Create a new log entry in the database.
    """
    log_entry_dict = log_entry.dict(by_alias=True)
    result = await db.logs.insert_one(log_entry_dict)
    log_entry.id = result.inserted_id
    return log_entry


async def get_logs(skip: int = 0, limit: int = 10) -> List[LogEntry]:
    """
    Retrieve a list of log entries from the database.
    """
    logs_cursor = db.logs.find().skip(skip).limit(limit)
    logs = await logs_cursor.to_list(length=limit)
    return [LogEntry(**log) for log in logs]


async def get_log_by_id(log_id: str) -> Optional[LogEntry]:
    """
    Retrieve a single log entry by its ID.
    """
    if not ObjectId.is_valid(log_id):
        return None
    log = await db.logs.find_one({"_id": ObjectId(log_id)})
    return LogEntry(**log) if log else None


async def update_log(log_id: str, log_entry: LogEntry) -> Optional[LogEntry]:
    """
    Update an existing log entry in the database.
    """
    if not ObjectId.is_valid(log_id):
        return None
    log_entry_dict = log_entry.dict(exclude_unset=True, by_alias=True)
    result = await db.logs.update_one(
        {"_id": ObjectId(log_id)},
        {"$set": log_entry_dict}
    )
    if result.modified_count == 1:
        updated_log = await db.logs.find_one({"_id": ObjectId(log_id)})
        return LogEntry(**updated_log) if updated_log else None
    return None


async def delete_log(log_id: str) -> bool:
    """
    Delete a log entry from the database.
    """
    if not ObjectId.is_valid(log_id):
        return False
    result = await db.logs.delete_one({"_id": ObjectId(log_id)})
    return result.deleted_count == 1


# Configuration CRUD Operations
async def create_configuration(configuration: Configuration):
    """
    Create a new configuration in the database.
    """
    config_dict = configuration.dict(by_alias=True)
    result = await db.configurations.insert_one(config_dict)
    configuration.id = result.inserted_id
    return configuration


async def get_configurations(skip: int = 0, limit: int = 10) -> List[Configuration]:
    """
    Retrieve a list of configurations from the database.
    """
    configs_cursor = db.configurations.find().skip(skip).limit(limit)
    configs = await configs_cursor.to_list(length=limit)
    return [Configuration(**config) for config in configs]


async def get_configuration_by_key(key: str) -> Optional[Configuration]:
    """
    Retrieve a single configuration by its key.
    """
    config = await db.configurations.find_one({"key": key})
    return Configuration(**config) if config else None


async def update_configuration(key: str, configuration: Configuration) -> Optional[Configuration]:
    """
    Update an existing configuration in the database.
    """
    config_dict = configuration.dict(exclude_unset=True, by_alias=True)
    result = await db.configurations.update_one(
        {"key": key},
        {"$set": config_dict}
    )
    if result.modified_count == 1:
        updated_config = await db.configurations.find_one({"key": key})
        return Configuration(**updated_config) if updated_config else None
    return None


async def delete_configuration(key: str) -> bool:
    """
    Delete a configuration from the database.
    """
    result = await db.configurations.delete_one({"key": key})
    return result.deleted_count == 1


# Large Model Response CRUD Operations
async def create_large_model_response(response: LargeModelResponse):
    """
    Create a new large model response in the database.
    """
    response_dict = response.dict(by_alias=True)
    result = await db.large_model_responses.insert_one(response_dict)
    response.id = result.inserted_id
    return response


async def get_large_model_responses(skip: int = 0, limit: int = 10) -> List[LargeModelResponse]:
    """
    Retrieve a list of large model responses from the database.
    """
    responses_cursor = db.large_model_responses.find().skip(skip).limit(limit)
    responses = await responses_cursor.to_list(length=limit)
    return [LargeModelResponse(**response) for response in responses]


async def get_large_model_response_by_id(response_id: str) -> Optional[LargeModelResponse]:
    """
    Retrieve a single large model response by its ID.
    """
    if not ObjectId.is_valid(response_id):
        return None
    response = await db.large_model_responses.find_one({"_id": ObjectId(response_id)})
    return LargeModelResponse(**response) if response else None


async def update_large_model_response(response_id: str, response: LargeModelResponse) -> Optional[LargeModelResponse]:
    """
    Update an existing large model response in the database.
    """
    if not ObjectId.is_valid(response_id):
        return None
    response_dict = response.dict(exclude_unset=True, by_alias=True)
    result = await db.large_model_responses.update_one(
        {"_id": ObjectId(response_id)},
        {"$set": response_dict}
    )
    if result.modified_count == 1:
        updated_response = await db.large_model_responses.find_one({"_id": ObjectId(response_id)})
        return LargeModelResponse(**updated_response) if updated_response else None
    return None


async def delete_large_model_response(response_id: str) -> bool:
    """
    Delete a large model response from the database.
    """
    if not ObjectId.is_valid(response_id):
        return False
    result = await db.large_model_responses.delete_one({"_id": ObjectId(response_id)})
    return result.deleted_count == 1


# Screenshot CRUD Operations
async def create_screenshot(screenshot: Screenshot):
    """
    Create a new screenshot in the database.
    """
    screenshot_dict = screenshot.dict(by_alias=True)
    result = await db.screenshots.insert_one(screenshot_dict)
    screenshot.id = result.inserted_id
    return screenshot


async def get_screenshots(skip: int = 0, limit: int = 10) -> List[Screenshot]:
    """
    Retrieve a list of screenshots from the database.
    """
    screenshots_cursor = db.screenshots.find().skip(skip).limit(limit)
    screenshots = await screenshots_cursor.to_list(length=limit)
    return [Screenshot(**screenshot) for screenshot in screenshots]


async def get_screenshot_by_id(screenshot_id: str) -> Optional[Screenshot]:
    """
    Retrieve a single screenshot by its ID.
    """
    if not ObjectId.is_valid(screenshot_id):
        return None
    screenshot = await db.screenshots.find_one({"_id": ObjectId(screenshot_id)})
    return Screenshot(**screenshot) if screenshot else None


async def update_screenshot(screenshot_id: str, screenshot: Screenshot) -> Optional[Screenshot]:
    """
    Update an existing screenshot in the database.
    """
    if not ObjectId.is_valid(screenshot_id):
        return None
    screenshot_dict = screenshot.dict(exclude_unset=True, by_alias=True)
    result = await db.screenshots.update_one(
        {"_id": ObjectId(screenshot_id)},
        {"$set": screenshot_dict}
    )
    if result.modified_count == 1:
        updated_screenshot = await db.screenshots.find_one({"_id": ObjectId(screenshot_id)})
        return Screenshot(**updated_screenshot) if updated_screenshot else None
    return None


async def delete_screenshot(screenshot_id: str) -> bool:
    """
    Delete a screenshot from the database.
    """
    if not ObjectId.is_valid(screenshot_id):
        return False
    result = await db.screenshots.delete_one({"_id": ObjectId(screenshot_id)})
    return result.deleted_count == 1


# User CRUD Operations
async def create_user(user: User):
    """
    Create a new user in the database.
    """
    user_dict = user.dict(by_alias=True)
    result = await db.users.insert_one(user_dict)
    user.id = result.inserted_id
    return user


async def get_users(skip: int = 0, limit: int = 10) -> List[User]:
    """
    Retrieve a list of users from the database.
    """
    users_cursor = db.users.find().skip(skip).limit(limit)
    users = await users_cursor.to_list(length=limit)
    return [User(**user) for user in users]


async def get_user_by_username(username: str) -> Optional[User]:
    """
    Retrieve a single user by their username.
    """
    user = await db.users.find_one({"username": username})
    return User(**user) if user else None


async def update_user(username: str, user: User) -> Optional[User]:
    """
    Update an existing user in the database.
    """
    user_dict = user.dict(exclude_unset=True, by_alias=True)
    result = await db.users.update_one(
        {"username": username},
        {"$set": user_dict}
    )
    if result.modified_count == 1:
        updated_user = await db.users.find_one({"username": username})
        return User(**updated_user) if updated_user else None
    return None


async def delete_user(username: str) -> bool:
    """
    Delete a user from the database.
    """
    result = await db.users.delete_one({"username": username})
    return result.deleted_count == 1