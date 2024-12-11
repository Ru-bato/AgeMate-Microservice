from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# 修改 tutorial-executor 路由，接受 request 参数
@app.get("/tutorial-executor")
def tutorial_executor(request: Request):
    return {"message": "Tutorial Executor API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
