# 用户管理系统 API 文档

## 概述
用户管理系统使用 OAuth2.0 + JWT 进行身份验证，支持用户注册、登录、账号管理等功能，区分管理员和普通用户权限。

## 数据设计
| 字段名         | 数据类型      | 描述                                            |
| ---------------| -------------|------------------------------------------------|
| `username`     | `VARCHAR(10)` | 用户名，非空（前端校验）,不重复。                     |
| `userID`       | `INTEGER`     | 自增主键，由数据库自动生成。                    |
| `password`     | `VARCHAR(255)`| 用户密码，后端转化并存储哈希值，原密码非空（前端校验）。      |
| `phone_number` | `CHAR(11)`    | 11 位手机号（数字）。                          |
| `authority`    | `SmallInteger`| 用户权限：0 表示管理员，1 表示普通用户。        |

## 基础 URL: http://localhost:8005

## 认证方式: Bearer Token 
认证 (Authentication) API 需要通过 Bearer Token 认证。示例如下：
请求头格式: Authorization: Bearer <your_token>

## 错误处理 (Error Handling)
API 返回的错误使用标准的 HTTP 状态码和 JSON 格式。示例错误响应：
```json
{
  "error_code": 401,
  "message": "Unauthorized - Invalid Token"
}
```
| 错误代码 | 错误代码描述       |
| -------- | ------------------ |
| 400      | 请求参数错误       |
| 401      | 未授权或认证失败   |
| 404      | 资源未找到         |
| 500      | 服务器内部错误     |

接口列表 (Endpoints)

---

## API 说明

### 公共接口
#### 1. 用户登录
**URL:** `/api/user/log`  
**方法:** `POST`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Content-Type`  | 否   | `application/json` |
**请求参数:**
```json
{
    "username": "string",
    "password": "string"
}
```
**响应:**
- 成功: `{"status": "success", "access_token": <token_string>}`
- 失败: `{"status": "failed"}`


#### 2. 账户找回
**URL:** `/api/user/findback`  
**方法:** `GET`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Content-Type`  | 否   | `application/json` |
**请求参数:**
```json
{
    "username": "string"
}
```
**响应:**
- 成功: `{"userID": "integer"}`
- 失败: `{"userID": ""}`
**错误处理 (Error Handling)**
不允许查找管理员账号
```json
{
  "error_code": 403,
  "message": "Insufficient permissions"
}
```


#### 3. 用户注册
**URL:** `/api/user/regist`  
**方法:** `POST`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Content-Type`  | 否   | `application/json` |
**请求参数:**
```json
{
    "username": "string",
    "password": "string",
    "phone_number": "string",
    "authority": "integer"
}
```
**响应:**
- 成功: `{"status": "success"}`
- 失败: `{"status": "failed"}`


---

### 用户接口（需登录）
#### 1. 获取账号信息
**URL:** `/api/user/account`  
**方法:** `GET`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Authorization` | 是   | Bearer <Token> |
**请求参数:**
```json
{
    "username": "string"
}
```
**响应:**
- 成功: 
```json
{
    "userID": "integer",
    "username": "string",
    "phone_number": "string",
    "authority": "integer"
}
```
- 失败: `{"status": "failed"}`
**错误处理 (Error Handling)**
不允许非管理员获取他人信息
```json
{
  "error_code": 403,
  "message": "You can only access your own account details"
}
```


#### 2. 修改账号信息
**URL:** `/api/user/changeAccount`  
**方法:** `POST`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Authorization` | 是   | Bearer <Token> |
**请求参数:**
```json
{
    "userID": "integer",
    "username": "string",
    "password": "string",
    "phone_number": "string",
    "authority": "integer"
}
```
**响应:**
- 成功: `{"status": "success"}`
- 失败: `{"status": "failed"}`
**错误处理 (Error Handling)**
不允许非管理员修改他人信息
```json
{
  "error_code": 403,
  "message": "You can only change your own account"
}
```


#### 3. 修改密码
**URL:** `/api/user/changePassword`  
**方法:** `POST`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Authorization` | 是   | <Bearer Token> |
| `Content-Type`  | 是   | `application/json` |
**请求参数:**
```json
{
    "userID": "integer",
    "password": "string"
}
```
**响应:**
- 成功: `{"status": "success"}`
- 失败: `{"status": "failed"}`
**错误处理 (Error Handling)**
不允许非管理员修改他人信息
```json
{
  "error_code": 403,
  "message": "You can only change your own account"
}
```


---

### 管理员接口（需登录，`authority = 0`）
#### 获取所有用户
**URL:** `/api/admin/users`  
**方法:** `GET`  
**请求头 (Headers):**
| 参数名         | 必填 | 描述               |
| -------------- | ---- | ------------------ |
| `Authorization` | 是   | Bearer <Token> |
**响应:**
```json
[
    {
        "userID": "integer",
        "username": "string",
        "phone_number": "string",
        "authority": "integer"
    }
]
```
**错误处理 (Error Handling)**
不允许非管理员获取全部用户信息
```json
{
  "error_code": 403,
  "message": "Insufficient permissions"
}
```


---

### 健康检查
**URL:** `/health`  
**方法:** `GET`  
**响应:**
- 成功: `{"status": "healthy"}`
- 失败: `{"status": "unhealthy"}`

---

## 示例代码 (Code Samples)

### 使用 cURL
```bash
curl -X GET "http://localhost:8005/api/user/log" \
     -H "Authorization: Bearer <your_token>"
```

### 使用 Python
```python
import requests

url = "http://localhost:8005/api/user/log"
headers = {"Authorization": "Bearer <your_token>"}
response = requests.get(url, headers=headers)

print(response.json())
```

---

## 版本控制 (Versioning)
当前版本通过文档说明，例如 v1.0。
每次发布新版本时，旧版本将继续支持至少 2 个月。

---

## 变更日志 (Changelog)
v1.0: 发布初始版本，包括用户登陆注册与信息修改,还有管理员管理用户信息等功能。