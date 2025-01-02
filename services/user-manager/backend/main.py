#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Developed by AlecNi @ 2024/12/29
# Description: Implementing a user management system with OAuth2.0 + JWT authentication.
# tested：
# 1. regist
# 2. log
# 3. health
# 4. admin get all users
# TODO:
# test other api
#

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, CHAR
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import secrets
from datetime import datetime, timedelta
from typing import Union, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

USER_BASE_URL = "/user-manager/api/user"
ADMIN_BASE_URL = "/user-manager/api/admin"

# Configuration for JWT and password hashing
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)  # Generate or fetch the secret key
ALGORITHM = "HS256"  # Algorithm used for encoding JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Database connection setup (replace with actual connection string)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqldb://agetutor:age123456@localhost:3306/user_manager_mysql")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OAuth2 configuration for Bearer Token extraction from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{USER_BASE_URL}/log")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Password hashing context

# FastAPI application initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端 URL
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# SQLAlchemy model for User
class User(Base):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # Auto-incremented user ID
    username = Column(String(10), index=True, unique=True, nullable=False)  # Username field (indexed and unique)
    password = Column(String(255), nullable=False)  # User password (hashed)
    phone_number = Column(CHAR(11), nullable=True)  # User phone number (11 digits)
    authority = Column(SmallInteger, nullable=False)  # User authority: 0 for admin, 1 for normal user

# Create database tables if not already present
Base.metadata.create_all(bind=engine, checkfirst=True)

# Pydantic model for user input during registration
class UserCreate(BaseModel):
    username: str
    password: str
    phone_number: str
    authority: int

# Pydantic model for user output during responses
class UserOut(BaseModel):
    userID: int
    username: str
    phone_number: str
    authority: int

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models

# JWT token generation function
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Set expiration time
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiration is 30 minutes
    to_encode.update({"exp": expire})  # Add expiration claim
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Generate JWT token
    return encoded_jwt

# Function to verify if a password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to extract and verify the JWT token from the request
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token
        return payload["sub"]  # Return the username from the token's payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")  # Token validation failed

# Function to verify if the current user is an admin (authority == 0)
def verify_admin_privileges(token: str = Depends(oauth2_scheme)) -> bool:
    user = get_current_user(token)
    db = SessionLocal()
    user_in_db = get_user_by_username(db, user)
    db.close()
    if user_in_db and user_in_db.authority == 0:  # 如果用户是管理员
        return True
    return False

# CRUD operation: Get user by username
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

# CRUD operation: Get user by userID
def get_user_by_id(db: Session, userID: int) -> Optional[User]:
    return db.query(User).filter(User.userID == userID).first()

# CRUD operation: Get all users for admin
def get_all_users(db: Session) -> list:
    users = db.query(User).all()
    return [UserOut.from_orm(user) for user in users]

# Dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to handle user login and JWT token generation
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post(f"{USER_BASE_URL}/log")
def log_request(login_request: LoginRequest, db: Session = Depends(get_db)) -> Dict[str, Union[str, bool]]:
    user = get_user_by_username(db, login_request.username)
    if user and verify_password(login_request.password, user.password):  # Validate username and password
        access_token = create_access_token(data={"sub": user.username})  # Create JWT token
        return {"status": "success", "access_token": access_token}  # Return token to the user
    return {"status": "failed"}  # Login failed

# API route to get user account details (requires valid JWT token)
class AccountRequest(BaseModel):
    username: str

@app.post(f"{USER_BASE_URL}/account")
def get_account(account_request: AccountRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_username(db, account_request.username)
    if user:
        return {"userID": user.userID, "phone_number": user.phone_number}  # Return user account details
    return {"status": "failed"}  # Invalid login or authorization

# API route to handle password recovery using username
class FindBackRequest(BaseModel):
    username: str

@app.post(f"{USER_BASE_URL}/findback")
def find_userID(findback_request: FindBackRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = get_user_by_username(db, findback_request.username)
    if user:
        return {"userID": str(user.userID)}  # Return userID if found
    return {"userID": "unknown"}  # Return "unknown" if user not found

# API route to handle user registration (creates a new user)
@app.post(f"{USER_BASE_URL}/regist")
def regist_request(user: UserCreate, db: Session = Depends(get_db)) -> Dict[str, str]:
    db_user = get_user_by_username(db, user.username)
    if db_user:
        return {"status": "failed"}  # Username already exists
    hashed_password = get_password_hash(user.password)  # Hash the password before saving
    db_user = User(username=user.username, password=hashed_password, phone_number=user.phone_number, authority=user.authority)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"status": "success"}  # Registration successful

# API route to change user account details (requires valid JWT token)
class ChangeAccountRequest(BaseModel):
    userID: int
    username: str
    password: str
    phone_number: str
    authority: int

@app.post(f"{USER_BASE_URL}/changeAccount")
def change_account(change_account_request: ChangeAccountRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_id(db, change_account_request.userID)
    if user:
        user.username = change_account_request.username
        user.password = get_password_hash(change_account_request.password)  # Hash the new password
        user.phone_number = change_account_request.phone_number
        user.authority = change_account_request.authority
        db.commit()  # Save the changes
        return {"status": "success"}
    return {"status": "failed"}  # User not found

# API route to change user password (requires valid JWT token)
class ChangePasswordRequest(BaseModel):
    userID: int
    password: str

@app.post(f"{USER_BASE_URL}/changePassword")
def change_password(change_password_request: ChangePasswordRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_id(db, change_password_request.userID)
    if user:
        user.password = get_password_hash(change_password_request.password)  # Hash and update password
        db.commit()
        return {"status": "success"}
    return {"status": "failed"}  # User not found

# API 路由：管理员查看所有用户
@app.get(f"{ADMIN_BASE_URL}/users")
def show_userlists(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_admin_privileges(token):  # 验证当前用户是否为管理员
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return get_all_users(db)  # 返回所有用户

# API 路由：管理员查看单个用户信息
@app.get(f"{ADMIN_BASE_URL}/acount")
def show_account(userID: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_admin_privileges(token):  # 验证当前用户是否为管理员
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    user = get_user_by_id(db, userID)
    if user:
        return {"userID": user.userID, "username": user.username, "phone_number": user.phone_number, "authority": user.authority}
    raise HTTPException(status_code=404, detail="User not found")

# API route to check the health of the database connection
@app.get("/health")
def health_check(db: Session = Depends(get_db)) -> Dict[str, str]:
    try:
        db.query(User).first()  # Test a simple query to check DB health
        return {"status": "healthy"}
    except Exception:
        return {"status": "unhealthy"}

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
