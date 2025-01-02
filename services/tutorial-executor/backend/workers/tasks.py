# -*- coding: utf-8 -*-
"""
Tasks

This module contains background tasks and asynchronous job processing logic for the application.
It uses FastAPI's BackgroundTasks for simple tasks and Celery for more complex, distributed task processing.
"""

from fastapi import BackgroundTasks
from celery import Celery
from models.crud import create_log_entry, create_large_model_response, create_screenshot, update_configuration
from models.schemas import LogEntry, LargeModelResponse, Screenshot, Configuration
import time
from typing import Dict, Any
import asyncio

# Initialize Celery with RabbitMQ as the broker
celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

# Optionally, configure Celery to use a results backend (e.g., Redis) if you need task result persistence
# celery_app.conf.result_backend = 'redis://localhost:6379/0'

# Optionally, configure task queues and routing
# from kombu import Queue
# celery_app.conf.task_queues = (
#     Queue('default', routing_key='task.#'),
#     Queue('long_running_tasks', routing_key='long_running_task.#'),
# )
# celery_app.conf.task_default_queue = 'default'
# celery_app.conf.task_default_exchange = 'tasks'
# celery_app.conf.task_default_routing_key = 'task.default'

# Example of a FastAPI BackgroundTask to log an entry after a response is sent
async def log_after_response(log_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Logs an entry using FastAPI's BackgroundTasks after sending a response.
    """
    background_tasks.add_task(create_log_entry, LogEntry(**log_data))

# Example of a Celery Task to simulate a long-running process
@celery_app.task(bind=True)
def simulate_long_running_process(self, task_id: str):
    """
    Simulates a long-running process that could be offloaded to a worker.
    """
    print(f"Starting long-running task {task_id}")
    time.sleep(10)  # Simulate a long-running process
    print(f"Completed long-running task {task_id}")

# Example of a Celery Task to generate a large model response
@celery_app.task
def generate_large_model_response(query: str) -> Dict[str, Any]:
    """
    Generates a large model response asynchronously.
    """
    # Simulate generating a response from a large model
    time.sleep(5)  # Simulate time taken to generate a response
    response_text = f"Response for query '{query}' generated."
    
    # Create a new LargeModelResponse entry in the database
    response_entry = LargeModelResponse(
        query=query,
        response=response_text,
        model_version="1.0"
    )
    asyncio.run(create_large_model_response(response_entry))  # Use asyncio.run to run async code in a sync context

    return response_entry.dict()

# Example of a Celery Task to capture and store a screenshot
@celery_app.task
def capture_and_store_screenshot(image_url: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Captures a screenshot and stores it in the database asynchronously.
    """
    # Simulate capturing a screenshot
    time.sleep(2)  # Simulate time taken to capture a screenshot
    
    # Create a new Screenshot entry in the database
    screenshot_entry = Screenshot(
        image_url=image_url,
        metadata=metadata
    )
    asyncio.run(create_screenshot(screenshot_entry))  # Use asyncio.run to run async code in a sync context

    return screenshot_entry.dict()

# Example of a Celery Task to periodically update configurations
@celery_app.task(bind=True)
def periodic_update_configurations(self, interval: int = 3600):
    """
    Periodically updates configurations based on external sources or checks.
    """
    while not self.request.revoked():
        print("Checking for configuration updates...")
        # Perform checks or fetch data from external sources here
        # For example purposes, we'll just update a dummy configuration
        dummy_config = Configuration(
            key="dummy_key",
            value={"some": "value"},
            description="Dummy configuration updated by periodic task."
        )
        asyncio.run(update_configuration(dummy_config.key, dummy_config))
        
        # Wait for the specified interval before checking again
        time.sleep(interval)

# Example of a Celery Task to clean up old entries
@celery_app.task
def cleanup_old_entries(retention_days: int = 30):
    """
    Cleans up old log entries and screenshots based on retention policy.
    """
    print("Starting cleanup of old entries...")
    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
    
    # Cleanup logs older than retention_days
    asyncio.run(db.logs.delete_many({"timestamp": {"$lt": cutoff_date}}))
    
    # Cleanup screenshots older than retention_days
    asyncio.run(db.screenshots.delete_many({"captured_at": {"$lt": cutoff_date}}))
    
    print("Cleanup completed.")

# Example of a FastAPI BackgroundTask to send notifications
async def send_notification(notification_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Sends a notification using FastAPI's BackgroundTasks.
    """
    background_tasks.add_task(_send_notification_async, notification_data)

async def _send_notification_async(notification_data: Dict[str, Any]):
    """
    Asynchronous function to send a notification.
    """
    print(f"Sending notification: {notification_data}")
    await asyncio.sleep(1)  # Simulate sending a notification
    print("Notification sent.")