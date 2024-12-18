import logging
import uvicorn
from fastapi import FastAPI
from interfaces.log_interface import log_router

# 初始化 FastAPI 应用
app = FastAPI()

# 注册路由
app.include_router(log_router)

logging.basicConfig(level=logging.DEBUG)
# 异步路由处理器
@app.get("/")
async def read_root():
    logging.debug("This is a debug message")
    return {"message": "Welcome to the Log Management API"}

# 主函数
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
