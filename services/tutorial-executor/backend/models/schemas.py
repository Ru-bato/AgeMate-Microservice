# -*- coding: utf-8 -*-
"""
Schemas

This module contains Pydantic models that define the data schemas for the application.
These schemas are used to validate and document the API requests and responses.
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from bson import ObjectId

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
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

# Log Entry schema with additional fields and validation
class LogEntry(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str
    message: str
    source: str
    context: Optional[Dict[str, Any]]  # Additional context information

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # Allows ObjectId
        json_encoders = {ObjectId: str}

# Configuration schema with extended metadata
class Configuration(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    key: str
    value: Any
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_assignment = True  # Validate on assignment

# Large model response with additional metadata
class LargeModelResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    query: str
    response: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model_version: str
    metadata: Dict[str, Any] = {}

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Screenshot with enhanced metadata and validation
class Screenshot(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    image_url: HttpUrl
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}
    tags: Optional[List[str]]

    @validator('image_url')
    def validate_image_url(cls, v):
        # Custom validation logic for the image URL can be added here
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Pagination schema for consistent API responses
class PaginatedResponse(BaseModel):
    items: List[Union[LogEntry, Configuration, LargeModelResponse, Screenshot]]
    total: int
    page: int
    size: int

    class Config:
        arbitrary_types_allowed = True

# User schema for authentication and authorization
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    full_name: Optional[str]
    disabled: Optional[bool] = False
    hashed_password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Token schema for JWT-based authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Error response schema for consistent error handling
class ErrorResponse(BaseModel):
    detail: str

class TaskRequest(BaseModel):
    model: str
    task: str
    website: str

class TaskStatus(BaseModel):
    id: str
    status: str
    result: Optional[str] = None
    
# Example usage of schemas (for testing purposes)
if __name__ == '__main__':
    log_entry = LogEntry(
        level="INFO",
        message="This is a test log entry.",
        source="app_module"
    )
    print(log_entry.json())

    config = Configuration(
        key="max_connections",
        value=100,
        description="Maximum number of database connections"
    )
    print(config.json())