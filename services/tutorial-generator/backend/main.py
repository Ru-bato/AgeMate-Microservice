from fastapi import FastAPI, Request
from rabbitmq.producer import RabbitMQProducer
import os
import uvicorn

BASE_URL = "/tutorial-generator"
app = FastAPI()
producer = None

@app.on_event("startup")
async def startup_event():
    global producer
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    producer = RabbitMQProducer(rabbitmq_url)

@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        await producer.close()

@app.post(f"{BASE_URL}/start-seeact")
async def start_seeact(task_data: dict):
    await producer.send_message(
        action="start_seeact",
        data=task_data
    )
    return {"status": "success", "message": "SeeAct task started"}
     
# 修改 tutorial-generator 路由，接受 request 参数
@app.get(f"{BASE_URL}/tutorial-generator")
def tutorial_generator(request: Request):
    return {"message": "Tutorial Generator API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get(f"{BASE_URL}/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
