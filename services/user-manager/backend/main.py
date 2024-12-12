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

from fastapi import FastAPI, Request
import uvicorn
import UserInfo
import registManager
import loginManager

app = FastAPI()

# TODO: import and invoke

# 修改 user-manager 路由，接受 request 参数
@app.get("/user-manager")
def user_manager(request: Request):
    return {"message": "User Manager API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
