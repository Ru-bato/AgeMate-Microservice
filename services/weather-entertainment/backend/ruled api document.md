# 天气子系统 API 文档

## 概述
天气子系统提供省份、城市、区域的查询接口，并支持通过地区编码获取实时天气、天气信息、以及天气预报数据，支持 GET 请求。

## 数据设计(主要字段解释)

| 字段名        | 数据类型    | 描述                                   |
| ------------- | ----------- | -------------------------------------- |
| `province`    | `string`    | 省份名称，用户提供，非空。             |
| `city`        | `string`    | 城市名称，用户提供，非空。             |
| `region`      | `string`    | 区域名称，用户提供，非空。             |
| `regionID`    | `string`    | 区域编码，系统返回，非空。             |
| `area_code`   | `string`    | 区域编码，系统返回，非空。             |
| `sk_data`     | `dict`      | 当前天气信息。                         |
| `city_info`   | `dict`      | 城市天气信息。                         |
| `forecast`    | `dict`      | 天气预报信息。                         |

## 基础 URL: `http://localhost:8006`

## 认证方式：`无认证，公开接口`

## 错误处理 (Error Handling)
API 返回的错误使用标准的 HTTP 状态码和 JSON 格式。
| 错误代码 | 错误代码描述             |
| -------- | ------------------------ |
| 400      | 请求参数错误             |
| 404      | 资源未找到               |
| 500      | 服务器内部错误           |

---

## 接口列表 (Endpoints)

### 公共接口

#### 1. 获取省份列表
**URL:** `/api/weather/province`  
**方法:** `POST`  
**响应:**
- 成功:
```python
["province1", "province2", ...]
```
- 失败:
```python
None
```


### 2. 获取城市列表
**URL:** `/api/weather/city`
**方法:** `POST`
**请求参数 (Query Parameters):**
```json
{
    "province": "string"
}
```
**响应:**
- 成功:
```python
["city1", "city2", ...]
```
- 失败:
```python
None
```


### 3. 获取区域列表
**URL:** `/api/weather/region`
**方法:** `POST`
**请求参数 (Query Parameters):**
```json
{
    "province": "string",
    "city": "string"
}
```
**响应:**
- 成功:
```python
["region1", "region2", ...]
```
- 失败:
```python
None
```


### 4. 获取区域编码
**URL:** `/api/weather/code`
**方法:** `POST`
**请求参数 (Query Parameters):**
```json
{
    "province": "string",
    "city": "string",
    "region": "string"
}
```
**响应:**
- 成功: `{"id": interger}`
- 失败: `{"error": "Province not found"/"City not found"/"Region not found"}`


### 5. 获取区域cityinfo天气信息
**URL:** `/api/weather/cityinfo`
**方法:** `POST`
**请求参数 (Query Parameters):**
```json
{
    "regionID": "string"
}
```
**响应:**
- 成功: `requests.get(url).json()`
```json
{
    "message": "success感谢又拍云(upyun.com)提供CDN赞助",
    "status": 200,
    "date": "20250103",
    "time": "2025-01-03 16:53:50",
    "cityInfo": {
        "city": "临海市",
        "citykey": "101210610",
        "parent": "台州市",
        "updateTime": "13:32"
    },
    "data": {
        "shidu": "46%",
        "pm25": 35.0,
        "pm10": 68.0,
        "quality": "良",
        "wendu": "11.9",
        "ganmao": "极少数敏感人群应减少户外活动",
        "forecast": [
            {
                "date": "03",
                "high": "高温 15℃",
                "low": "低温 2℃",
                "ymd": "2025-01-03",
                "week": "星期五",
                "sunrise": "06:49",
                "sunset": "17:10",
                "aqi": 66,
                "fx": "北风",
                "fl": "1级",
                "type": "晴",
                "notice": "愿你拥有比阳光明媚的心情"
            },
            ...
        ]
    }
}
```
- 失败: `{"error": "Weather data not found"}`


<!-- ### 6. 获取区域sk天气信息
**URL:** `/api/weather/sk`
**方法:** `GET`
**请求参数 (Query Parameters):**
```json
{
    "regionID": "string"
}
```
**响应:**
- 成功: `requests.get(url).json()`
- 失败: `{"error": "Weather data not found"}`


### 7. 获取区域forecast天气信息
**URL:** `/api/weather/forecast`
**方法:** `GET`
**请求参数 (Query Parameters):**
```json
{
    "regionID": "string"
}
```
**响应:**
- 成功: `requests.get(url).json()`
- 失败: `{"error": "Weather data not found"}` -->


---

### 健康检查
**URL:** `/health`  
**方法:** `GET`  
**响应:**
- `{"status": "healthy"}`


---

## 示例代码 (Code Samples)
### 使用 cURL
```bash
curl -X GET "http://localhost:8006/api/weather/province"
```
```python
import requests

url = "http://localhost:8006/api/weather/province"
response = requests.get(url)

print(response.json())
```


---

## 版本控制 (Versioning)
当前版本为 v1.0，后续版本更新时将继续支持至少 2 个月。


---

## 变更日志 (Changelog)
v1.0: 发布初始版本，包括获取省份、城市、区域、区域编码、当前天气、天气预报和城市天气等功能。


---

## 注意事项
API 请求没有认证机制（例如 JWT 或 OAuth2），因此数据的使用应该遵循公共接口的相关规则。
由于接口是通过外部天气服务获取数据，服务不稳定时会出现失败的情况，调用时需要处理网络错误和 API 响应失败的情况。