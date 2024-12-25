import asyncio
import os
import logging
from fastapi import FastAPI, BackgroundTasks, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from seeact import main as seeact_main
from fastapi.logger import logger as fastapi_logger
import uvicorn
from rabbitmq.consumer import RabbitMQConsumer

# 确保可以找到本地的 seeact.py 文件
sys.path.append(os.path.join(os.path.dirname(__file__), "path_to_seeact_directory"))

BASE_URL = "/tutorial-executor"
app = FastAPI()
background_tasks = BackgroundTasks()

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

# Logging setup
logger = logging.getLogger(__name__)
# fastapi_logger.handlers = logger.handlers
# fastapi_logger.setLevel(logging.INFO)  # Ensure logs are captured
logger.setLevel(logging.INFO)

# Logging middleware to log all requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# TODO: 补全
@app.on_event("startup")
async def startup_event():
    # 获取 RabbitMQ URL
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    
    # 创建 RabbitMQ 消费者
    consumer = RabbitMQConsumer(
        rabbitmq_url=rabbitmq_url,
        background_tasks=background_tasks,
        run_seeact=run_seeact
    )
    
    # 启动消费者
    await consumer.start()

@app.get(f"{BASE_URL}/start-seeact")
async def start_seeact(background_tasks: BackgroundTasks):
    """
    启动 SeeAct 任务
    """
    logger.info("Starting SeeAct task in the background.")
    background_tasks.add_task(run_seeact)
    return {"message": "SeeAct task has been started."}

# For test
@app.get(f"{BASE_URL}")
def guidebook_generator(request: Request):
    return {"message": "Tutorial Executor API"}

# Health check endpoint
@app.get(f"{BASE_URL}/health")
def health_check():
    return {"status": "ok"}

# Exception handler
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )

# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

async def run_seeact():
    """
    在后台异步运行 seeact.py 的 main 函数
    """
    logger.info("Inside run_seeact")
    
    # 配置文件路径
    config_path = os.path.join(os.path.dirname(__file__), "config", "demo_mode.toml")
    
    # 加载配置
    config = None
    try:
        with open(config_path, 'r') as toml_config_file:
            import toml
            config = toml.load(toml_config_file)
            logger.info(f"Configuration File Loaded - {config_path}")
    except FileNotFoundError:
        logger.error(f"Error: File '{config_path}' not found.")
        return
    except toml.TomlDecodeError:
        logger.error(f"Error: File '{config_path}' is not a valid TOML file.")
        return

    # 调用 seeact 的 main 函数
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"base_dir: {base_dir}")
        await seeact_main(config, base_dir)
    except Exception as e:
        logger.error(f"Error in SeeAct main execution: {str(e)}")
        logger.error("详细错误信息:", exc_info=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
