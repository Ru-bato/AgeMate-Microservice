import asyncio
import os
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi import FastAPI, Request, BackgroundTasks, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from seeact import main as seeact_main
from fastapi.logger import logger as fastapi_logger

# 确保可以找到本地的 seeact.py 文件
sys.path.append(os.path.join(os.path.dirname(__file__), "path_to_seeact_directory"))

# 导入 seeact.py 中的 main 函数
from seeact import main as seeact_main

BASE_URL = "/tutorial-executor"
app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming a frontend dev server at this address
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# More detailed logging
logger = logging.getLogger(__name__)
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")

fastapi_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.setLevel(gunicorn_logger.level)
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
uvicorn_access_logger.setLevel(gunicorn_logger.level)

# Logging middleware to log all requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.post(f"{BASE_URL}/start-seeact")
async def start_seeact(background_tasks: BackgroundTasks):
    """
    启动 SeeAct 任务
    """
    background_tasks.add_task(run_seeact)
    return {"message": "SeeAct task has been started."}

# For test
@app.get(BASE_URL)
def guidebook_generator(request: Request):
    return {"message": "Tutorial Executor API"}

# Exception handler
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )

# Exception handler for HTTPException (can be used for 4xx or 5xx errors)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},  # or just exc.detail if you prefer
    )

async def run_seeact():
    """
    在后台异步运行 seeact.py 的 main 函数
    """
    # 配置文件路径
    config_path = os.path.join(os.path.dirname(__file__), "config", "demo_mode.toml")
    
    # 加载配置
    config = None
    try:
        with open(config_path, 'r') as toml_config_file:
            import toml
            config = toml.load(toml_config_file)
            print(f"Configuration File Loaded - {config_path}")
    except FileNotFoundError:
        print(f"Error: File '{config_path}' not found.")
    except toml.TomlDecodeError:
        print(f"Error: File '{config_path}' is not a valid TOML file.")
        return

    # 调用 seeact 的 main 函数
    base_dir = os.path.dirname(os.path.abspath(__file__))
    await seeact_main(config, base_dir)
