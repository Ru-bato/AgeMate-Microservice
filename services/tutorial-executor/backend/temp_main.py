# # -*- coding: utf-8 -*-
# """
# SeeAct FastAPI Application Entry Point

# This file initializes the FastAPI application, sets up middleware,
# and includes routers for different endpoints.
# """

# import logging
# from fastapi import FastAPI, Request, BackgroundTasks, status, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from config.settings import settings
# from routes import web_actions, inference, other_routes
# from models.database import get_db, close_db_connection
# from config.logging import setup_logging
# from fastapi.openapi.utils import get_openapi
# from workers.tasks import celery_app  # 导入Celery应用实例
# from config.settings import settings
# from routes import web_actions
# from fastapi.logger import logger as fastapi_logger

# BASE = "/tutorial-executor"
# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     description="Tutorial Executor Microservice, which can automatically control the webpage like human.",
#     version=settings.API_VERSION,
# )

# app.include_router(web_actions.router)
# # Setup logging
# setup_logging(settings)

# # Initialize database connection
# @app.on_event("startup")
# async def startup_event():
#     async with get_db():
#         print("Database initialized.")
#     # Optionally initialize Celery worker here if needed
#     # from app.workers.tasks import celery_app
#     # celery_app.control.ping()  # Check Celery workers

# # Close database connection on shutdown
# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db_connection()
#     print("Database connection closed.")

# # CORS Middleware
# origins = [
#     "http://localhost",
#     "http://localhost:3000",  # Assuming a frontend dev server at this address
#     # Add more origins as needed
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Exception handler
# @app.exception_handler(Exception)
# async def validation_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"message": str(exc)},
#     )

# # Exception handler for HTTPException (can be used for 4xx or 5xx errors)
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": str(exc.detail)},  # or just exc.detail if you prefer
#     )


# # Custom OpenAPI configuration
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=settings.PROJECT_NAME,
#         version=settings.API_VERSION,
#         description="SeeAct FastAPI API Documentation",
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://example.com/logo.png"  # Replace with actual logo URL
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi

# # Include routers
# app.include_router(web_actions.router, prefix="/tutorial-executor/webactions", tags=["Web Actions"])
# app.include_router(inference.router, prefix="/tutorial-executor/inference", tags=["Inference"])
# app.include_router(other_routes.router, prefix="/tutorial-executor/other", tags=["Other"])

# # Health check endpoint with detailed health information
# @app.get("/tutorial-executor/health", status_code=status.HTTP_200_OK)
# async def health_check():
#     db_status = "healthy" if await check_db_health() else "unhealthy"
#     return {"status": "healthy", "db_status": db_status}

# async def check_db_health():
#     try:
#         # Perform a simple query to test database connectivity
#         await client.test_collection.find_one()
#         return True
#     except Exception:
#         return False

# # Background tasks management (using Celery for reliable task queueing)
# @app.post("/send-notification/{email}")
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#     # Use Celery for background tasks in production environments
#     celery_app.send_task('tasks.write_notification', args=[email, "some notification"])
#     return {"message": "Notification sent in the background"}

# # More detailed logging
# logger = logging.getLogger(__name__)
# gunicorn_error_logger = logging.getLogger("gunicorn.error")
# gunicorn_logger = logging.getLogger("gunicorn")
# uvicorn_access_logger = logging.getLogger("uvicorn.access")

# fastapi_logger.handlers = gunicorn_error_logger.handlers
# fastapi_logger.setLevel(gunicorn_logger.level)
# uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
# uvicorn_access_logger.setLevel(gunicorn_logger.level)

# # Logging middleware to log all requests and responses
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Request: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Response: {response.status_code}")
#     return response

# # Optional: Add more endpoints or configurations here

# # for test
# @app.get("/tutorial-executor")
# def guidebook_generator(request: Request):
#     return {"message": "Tutorial Executor API"}


# def load_config():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-c", "--config_path", help="Path to the TOML configuration file.", type=str, metavar='config',
#                         default=f"{os.path.join('config', 'demo_mode.toml')}")
#     args = parser.parse_args()
#     # Load configuration file
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     config = None
#     try:
#         with open(os.path.join(base_dir, args.config_path) if not os.path.isabs(args.config_path) else args.config_path,
#                   'r') as toml_config_file:
#             config = toml.load(toml_config_file)
#             print(f"Configuration File Loaded - {os.path.join(base_dir, args.config_path)}")
#     except FileNotFoundError:
#         print(f"Error: File '{args.config_path}' not found.")
#     except toml.TomlDecodeError:
#         print(f"Error: File '{args.config_path}' is not a valid TOML file.")
    
#     return config, base_dir

# @app.post("{BASE}/executor-start")
# def tutorial_executor_start(request: Request):
#     load_config() # TODO: async?
    