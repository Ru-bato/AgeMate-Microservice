# import os
# from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends, status
# from fastapi.responses import JSONResponse
# import toml
# from pathlib import Path
# from prometheus_fastapi_instrumentator import Instrumentator
# from utils.redis_client import get_redis_client  # 新增：Redis客户端
# from utils.mongo_logger import setup_mongo_logger  # 新增：MongoDB日志配置
# from utils.rabbitmq_publisher import publish_to_rabbitmq  # 新增：RabbitMQ消息发布器
# import uuid

# BASE_URL = "/tutorial-executor"
# # Initialize logger with MongoDB handler
# logger = setup_mongo_logger(db_name="logs_db", collection_name="api_logs")

# app = FastAPI()

# # Initialize Prometheus monitoring
# Instrumentator().instrument(app).expose(app)
# base_dir = os.path.dirname(os.path.abspath(__file__))
# def get_config():
#     """Load configuration from TOML file."""
#     base_dir = Path(__file__).resolve().parent
#     config_path = base_dir / "config" / "demo_mode.toml"
#     try:
#         with open(config_path, 'r') as toml_config_file:
#             config = toml.load(toml_config_file)
#             print(f"Configuration File Loaded - {config_path}")
#             return config
#     except FileNotFoundError:
#         print(f"Error: File '{config_path}' not found.")
#     except toml.TomlDecodeError:
#         print(f"Error: File '{config_path}' is not a valid TOML file.")


# @app.post(f"{BASE_URL}/start_task/", status_code=status.HTTP_200_OK)
# async def start_task(
#     background_tasks: BackgroundTasks,
#     request: Request,
#     config=Depends(get_config),
#     redis_client=Depends(get_redis_client)  # 使用依赖注入获取Redis客户端
# ):
#     """
#     API endpoint to start a web automation task.
    
#     Args:
#         background_tasks (BackgroundTasks): FastAPI's BackgroundTasks object.
#         request (Request): The incoming HTTP request.
#         config (dict): Configuration loaded from TOML file.
#         redis_client (redis.Redis): Redis client for state management.
        
#     Returns:
#         JSONResponse: Response indicating the task has been scheduled.
#     """
#     try:
#         data = await request.json()
#         task_input = data.get("task", "")
#         website_input = data.get("website", "")

#         if not task_input or not website_input:
#             raise ValueError("Task and website are required.")

#         task_id = str(uuid.uuid4())  # Generate a unique ID for this task
#         task_data = {"id": task_id, "task": task_input, "website": website_input}
        
#         # Store the task in Redis with its initial state (e.g., "pending")
#         redis_client.set(task_id, "pending")

#         # Publish the task data to RabbitMQ
#         await publish_to_rabbitmq(toml.dumps(task_data))

#         # Log the event
#         logger.info(f"Task {task_id} has been scheduled.")

#         return JSONResponse(content={"message": "Task published to RabbitMQ.", "task_id": task_id})
#     except Exception as e:
#         logger.error(f"Error in /start_task/: {str(e)}")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))