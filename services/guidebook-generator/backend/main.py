import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from interfaces.log_interface import log_router

# 初始化 FastAPI 应用
app = FastAPI()
# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法（如 GET, POST, PUT, DELETE 等）
    allow_headers=["*"],  # 允许所有请求头
)
# 注册路由
app.include_router(log_router)

# 异步路由处理器
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Log Management API"}

# 主函数
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
