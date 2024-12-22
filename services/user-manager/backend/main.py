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
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, constr
from contextlib import contextmanager
from typing import Union, Dict

# MySQL Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://user:password@localhost:3306/db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app initialization
app = FastAPI()

# SQLAlchemy model
class User(Base):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True, autoincrement=True)  # userID为自增整数
    username = Column(String(10), index=True)
    password = Column(String(20))
    phone_number = Column(String(11))
    authority = Column(TINYINT)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic schema for user
# Pydantic schema for user
class UserCreate(BaseModel):
    username: str
    password: str
    phone_number: str
    authority: int

class UserOut(BaseModel):
    userID: str
    username: str
    authority: int

    class Config:
        orm_mode = True

# Dependency for getting DB session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_userID(db, userID: str):
    return db.query(User).filter(User.userID == userID).first()

def create_user(db, user: UserCreate):
    db_user = User(username=user.username, password=user.password, 
                   phone_number=user.phone_number, authority=user.authority)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_account(db, userID: str, username: str, password: str, authority: int):
    db_user = db.query(User).filter(User.userID == userID).first()
    if db_user:
        db_user.username = username
        db_user.password = password
        db_user.authority = authority
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def findback_userID(db, username: str, phone_number: str):
    return db.query(User).filter(User.username == username, User.phone_number == phone_number).first()

def change_password(db, userID: str, password: str):
    db_user = db.query(User).filter(User.userID == userID).first()
    if db_user:
        db_user.password = password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

# API Routes
@app.get("/api/user/log")
def log_request(username: str, password: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = get_user_by_username(db, username)
    if user and user.password == password:
        return {"status": "true"}
    return {"status": "false"}

@app.get("/api/user/account")
def get_account(username: str, password: str, db: Session = Depends(get_db)) -> Union[Dict[str, Union[str, int]], Dict[str, str]]:
    user = get_user_by_username(db, username)
    if user and user.password == password:
        return {"userID": str(user.userID), "authority": user.authority}
    return {"status": "false"}

@app.get("/api/user/findback")
def find_userID(username: str, phone_number: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    # 根据用户名和手机号查找用户
    user = findback_userID(db, username, phone_number)
    if user:
        # 找到用户，返回 userID
        return {"userID": str(user.userID)}
    else:
        # 未找到用户，返回 "unknown"
        return {"userID": "unknown"}

@app.post("/api/user/regist")
def regist_request(user: UserCreate, db: Session = Depends(get_db)) -> Dict[str, str]:
    # 检查用户名是否已存在
    db_user = get_user_by_username(db, user.username)
    if db_user:
        return {"status": "failed"}
    create_user(db=db, user=user)
    return {"status": "success"}

@app.post("/api/user/changeAccount")
def change_account(userID: str, username: str, password: str, authority: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = update_account(db=db, userID=userID, username=username, password=password, authority=authority)
    if user:
        return {"status": "success"}
    return {"status": "failed"}

@app.post("/api/user/changePassword")
def change_password_endpoint(userID: str, password: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = change_password(db=db, userID=userID, password=password)
    if user:
        return {"status": "success"}
    return {"status": "failed"}

@app.get("/api/user/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  # 测试数据库连接
        return {"status": "success"}
    except Exception:
        return {"status": "failed"}

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
