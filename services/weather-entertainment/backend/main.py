#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Developed by AlecNi @ 2025/1/2
# Description: Implementing weather subsystem
# tested：
# 1. get province
# 2. get city
# 3. get region
# 4. get region id
# 5. get forecast data(by day)
# TODO:
# 6. get more specific data

import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from fastapi.middleware.cors import CORSMiddleware

WEATHER_BASE_URL = "/api/weather"
WEATHER_EXTENAL_ID_URL = "http://www.weather.com.cn/data/city3jdata"
WEATHER_EXTENAL_URL = "http://t.weather.itboy.net/api/weather"
ENTERTAINMENT_BASE_URL = "/api/entertainment"

# FastAPI app initialization
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # You can replace with "*" to get low-couple
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端 URL
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# # OpenWeatherMap API Key (replace with your actual key)
# API_KEY = "your_api_key"  # Replace with your API key

# Model to define the input for the weather query
class CityRequest(BaseModel):
    province: str
    city: str
    region: str

# 获取省份ID
def get_province(province_name: str) -> Optional[str]:
    url = f"{WEATHER_EXTENAL_ID_URL}/china.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        provinces = response.json()
        for id, name in provinces.items():
            if name == province_name:
                return id
    return None

# 获取城市ID
def get_city(province_id: str, city_name: str) -> Optional[str]:
    url = f"{WEATHER_EXTENAL_ID_URL}/provshi/{province_id}.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        cities = response.json()
        for id, name in cities.items():
            if name == city_name:
                return province_id + id
    return None

# 获取区域ID
def get_region(city_id: str, region_name: str) -> Optional[str]:
    url = f"{WEATHER_EXTENAL_ID_URL}/station/{city_id}.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        regions = response.json()
        for id, name in regions.items():
            if name == region_name:
                if city_id[5:7] == "00":
                    return city_id[:5] + id + "00"
                else:
                    return city_id + id
    return None

# # 获取天气信息sk
# def get_weather_sk(area_code: str) -> Dict[str, Any]:
#     url = f"{WEATHER_EXTENAL_URL}/sk/{area_code}.html"
#     response = requests.get(url)
#     # 显式设置响应的编码为 UTF-8
#     response.encoding = 'utf-8'
#     if response.status_code == 200:
#         return response.json()
#     return {}

# 获取天气信息cityinfo
def get_weather_cityinfo(area_code: str) -> Dict[str, Any]:
    url = f"{WEATHER_EXTENAL_URL}/city/{area_code}"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.json()
    return {}

# # 获取天气信息
# def get_weather_forecast(area_code: str) -> Dict[str, Any]:
#     url = f"{WEATHER_EXTENAL_URL}/{area_code}.html"
#     response = requests.get(url)
#     # 显式设置响应的编码为 UTF-8
#     response.encoding = 'utf-8'
#     if response.status_code == 200:
#         return response.json()
#     return {}

# Endpoint to get weather information based on province, city, and region
@app.get(f"{WEATHER_BASE_URL}/province")
async def weather_province() -> List[str]:
    """
    :return: province code
    """
    url = f"{WEATHER_EXTENAL_ID_URL}/china.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        provinces = response.json()
        provinces_list = [name for id, name in provinces.items()]
        return provinces_list
    return None

class Province(BaseModel):
    province: str

# Endpoint to get weather information based on province, city, and region
@app.post(f"{WEATHER_BASE_URL}/city")
async def weather_city(known: Province) -> List[str]:
    """
    :return: city code
    """
    province_id = get_province(known.province)
    if province_id is None:
        return None
    
    url = f"{WEATHER_EXTENAL_ID_URL}/provshi/{province_id}.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        cities = response.json()
        cities_list = [name for id, name in cities.items()]
        return cities_list
    return None

class City(BaseModel):
    province: str
    city: str

# Endpoint to get weather information based on province, city, and region
@app.post(f"{WEATHER_BASE_URL}/region")
async def weather_region(known: City) -> List[str]:
    """
    :return: region code
    """
    province_id = get_province(known.province)
    city_id = get_city(province_id, known.city)
    if city_id is None:
        return None
    
    url = f"{WEATHER_EXTENAL_ID_URL}/station/{city_id}.html"
    response = requests.get(url)
    # 显式设置响应的编码为 UTF-8
    response.encoding = 'utf-8'
    if response.status_code == 200:
        regions = response.json()
        regions_list = [name for id, name in regions.items()]
        return regions_list
    return None

# Endpoint to get weather information based on province, city, and region
@app.post(f"{WEATHER_BASE_URL}/code")
async def weather_code(request: CityRequest) -> Dict[str, Any]:
    """
    根据输入的省名称、市名称、地区名称获取编码
    :param request: The request body containing province, city, and region
    :return: region code
    """
    # 获取省份ID
    province_id = get_province(request.province)
    if not province_id:
        return {"error": "Province not found"}
    
    # 获取城市ID
    city_id = get_city(province_id, request.city)
    if not city_id:
        return {"error": "City not found"}
    
    # 获取区域ID
    region_id = get_region(city_id, request.region)
    if not region_id:
        return {"error": "Region not found"}
    
    return {"id": region_id}

class RegionID(BaseModel):
    regionID: str

# # Endpoint to get weather information based on province, city, and region
# @app.get(f"{WEATHER_BASE_URL}/sk")
# async def weather_sk(request: RegionID) -> Dict[str, Any]:
#     """
#     根据输入的地区编码获取天气信息
#     :param request: The request body containing regionID
#     :return: A JSON response containing the weather information
#     """    
#     # 获取天气数据
#     weather_data = get_weather_sk(request.regionID)
#     if not weather_data:
#         return {"error": "Weather data not found"}
    
#     return weather_data

# Endpoint to get weather information based on province, city, and region
@app.post(f"{WEATHER_BASE_URL}/cityinfo")
async def weather_cityinfo(request: RegionID) -> Dict[str, Any]:
    """
    根据输入的地区编码获取天气信息
    :param request: The request body containing regionID
    :return: A JSON response containing the weather information
    """
    # 获取天气数据
    weather_data = get_weather_cityinfo(request.regionID)
    if not weather_data and weather_data['status'] == 200:
        return {"error": "Weather data not found"}
    
    return weather_data

# # Endpoint to get weather information based on province, city, and region
# @app.get(f"{WEATHER_BASE_URL}/forecast")
# async def weather_forecast(request: RegionID) -> Dict[str, Any]:
#     """
#     根据输入的地区编码获取天气预测信息
#     :param request: The request body containing regionID
#     :return: A JSON response containing the weather information
#     """
#     # 获取天气数据
#     weather_data = get_weather_forecast(request.regionID)
#     if not weather_data:
#         return {"error": "Weather data not found"}
    
#     return weather_data

# Health check endpoint to check if the service is running
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Check if the service is healthy and running.
    :return: A JSON response indicating the service status
    """
    return {"status": "healthy"}

# Entry point for running the app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)
