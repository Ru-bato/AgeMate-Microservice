from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# 修改 log-manager 路由，接受 request 参数
@app.get("/log-manager")
def log_manager(request: Request):
    return {"message": "Log Manager API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
