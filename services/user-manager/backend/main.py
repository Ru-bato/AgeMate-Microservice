#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Developed by AlecNi @ 2024/12/12
# Description:
#   the backend program of the log-manager
# Solved:
# Unsolved:
#   1.userInfo Struct
#   2.login method
#   3.regist method
#   else

import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import aio_pika
# 用于指明返回类型
from typing import List, Dict

# 读取环境变量
DATABASE_URL = os.getenv("DATABASE_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

# 初始化 FastAPI 应用
app = FastAPI()

# 数据库连接
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# RabbitMQ 连接
rabbitmq_connection = None


@app.on_event("startup")
async def startup_event() -> None:
    global rabbitmq_connection
    try:
        # 连接 RabbitMQ
        rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event() -> None:
    global rabbitmq_connection
    if rabbitmq_connection:
        await rabbitmq_connection.close()


# 健康检查接口
@app.get("/health")
async def health_check() -> Dict[str, str]:
    try:
        # 检查数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        # 检查 RabbitMQ 连接
        if rabbitmq_connection and rabbitmq_connection.is_closed:
            raise HTTPException(status_code=500, detail="RabbitMQ connection closed")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 示例 API：查询用户表中的数据
@app.get("/users")
async def get_users() -> Dict[str, List[Dict[str, str]]]:
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT * FROM users")).fetchall()
            return {"users": [dict(row) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 示例 API：发送消息到 RabbitMQ
@app.post("/send-message")
async def send_message(message: str) -> Dict[str, str]:
    try:
        async with rabbitmq_connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key="example_queue",
            )
        return {"status": "message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 路由：获取表中的所有数据
@app.get("/items/")
async def read_items() -> List[Dict]:
    with engine.connect() as conn:
        query = select([example_table])
        result = conn.execute(query)
        items = [dict(row) for row in result]
    return items


# 路由：根据 ID 查询数据
@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Dict:
    with engine.connect() as conn:
        query = select([example_table]).where(example_table.c.id == item_id)
        result = conn.execute(query).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(result)


# TODO: import and invoke


# 修改 user-manager 路由，接受 request 参数
@app.get("/user-manager")
def user_manager(request: Request) -> Dict[str, str]:
    return {"message": "User Manager API"}

@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
