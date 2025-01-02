# -*- coding: utf-8 -*-
"""
Database Utilities

This module contains utility functions and classes for interacting with MongoDB.
It provides functionalities such as connecting to the database, executing CRUD operations,
and handling transactions.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from contextlib import asynccontextmanager
from config.settings import settings
from typing import Any, Dict, List, Optional
import logging

client = AsyncIOMotorClient(str(settings.MONGODB_URL))
db_name = settings.MONGODB_DB_NAME

@asynccontextmanager
async def get_db():
    """
    Async context manager that yields a reference to the MongoDB database.
    Ensures proper resource management.
    
    Yields:
        AsyncIOMotorDatabase: A reference to the MongoDB database.
    """
    try:
        yield client[db_name]
    except Exception as e:
        logging.error(f"An error occurred while accessing the database: {e}")
        raise
    finally:
        # Motor manages its own connection pool; no explicit close needed here
        pass

@asynccontextmanager
async def close_db_connection():
    pass

class DatabaseUtils:
    def __init__(self, db=Depends(get_db)):
        self.db = db

    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Finds a single document in the specified collection matching the query.

        Args:
            collection (str): The name of the collection.
            query (Dict[str, Any]): The query to match documents against.

        Returns:
            Optional[Dict[str, Any]]: The found document or None if not found.
        """
        return await self.db[collection].find_one(query)

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> Any:
        """
        Inserts a new document into the specified collection.

        Args:
            collection (str): The name of the collection.
            document (Dict[str, Any]): The document to insert.

        Returns:
            Any: Inserted document's ID.
        """
        result = await self.db[collection].insert_one(document)
        return result.inserted_id

    async def update_one(self, collection: str, filter_query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Updates a single document in the specified collection based on a filter query.

        Args:
            collection (str): The name of the collection.
            filter_query (Dict[str, Any]): The query to match documents against.
            update_data (Dict[str, Any]): The data to update.

        Returns:
            int: The number of modified documents.
        """
        result = await self.db[collection].update_one(filter_query, {"$set": update_data})
        return result.modified_count

    async def delete_one(self, collection: str, filter_query: Dict[str, Any]) -> int:
        """
        Deletes a single document from the specified collection based on a filter query.

        Args:
            collection (str): The name of the collection.
            filter_query (Dict[str, Any]): The query to match documents against.

        Returns:
            int: The number of deleted documents.
        """
        result = await self.db[collection].delete_one(filter_query)
        return result.deleted_count

    async def find(self, collection: str, query: Dict[str, Any], projection: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Finds multiple documents in the specified collection matching the query.

        Args:
            collection (str): The name of the collection.
            query (Dict[str, Any]): The query to match documents against.
            projection (Optional[Dict[str, Any]]): The fields to include or exclude. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of found documents.
        """
        cursor = self.db[collection].find(query, projection)
        documents = await cursor.to_list(length=None)
        return documents