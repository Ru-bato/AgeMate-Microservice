import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

WEATHER_BASE_URL = "/api/weather"
ENTERTAINMENT_BASE_URL = "/api/entertainment"

# FastAPI app initialization
app = FastAPI()

# # OpenWeatherMap API Key (replace with your actual key)
# API_KEY = "your_api_key"  # Replace with your API key

# Model to define the input for the weather query
class CityRequest(BaseModel):
    province: str
    city: str
    region: str

# 获取省份ID
def get_state(province_name: str) -> Optional[str]:
    url = "http://www.weather.com.cn/data/city3jdata/china.html"
    response = requests.get(url)
    if response.status_code == 200:
        provinces = response.json()
        for province in provinces:
            if province['name'] == province_name:
                return province['id']
    return None

# 获取城市ID
def get_city(province_id: str, city_name: str) -> Optional[str]:
    url = f"http://www.weather.com.cn/data/city3jdata/provshi/{province_id}.html"
    response = requests.get(url)
    if response.status_code == 200:
        cities = response.json()
        for city in cities:
            if city['name'] == city_name:
                return province_id + city['id']
    return None

# 获取区域ID
def get_region(province_id: str, city_id: str, region_name: str) -> Optional[str]:
    url = f"http://www.weather.com.cn/data/city3jdata/station/{province_id}{city_id}.html"
    response = requests.get(url)
    if response.status_code == 200:
        regions = response.json()
        for region in regions:
            if region['name'] == region_name:
                return province_id + city_id + region['id']
    return None

# 获取天气信息sk
def get_weather_sk(area_code: str) -> Dict[str, Any]:
    url = f"http://m.weather.com.cn/data/sk/{area_code}.html"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# 获取天气信息cityinfo
def get_weather_cityinfo(area_code: str) -> Dict[str, Any]:
    url = f"http://m.weather.com.cn/data/cityinfo/{area_code}.html"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# 获取天气信息
def get_weather_forecast(area_code: str) -> Dict[str, Any]:
    url = f"http://m.weather.com.cn/data/{area_code}.html"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Endpoint to get weather information based on province, city, and region
@app.get(f"{WEATHER_BASE_URL}/sk")
async def weather_sk(request: CityRequest) -> Dict[str, Any]:
    """
    根据输入的省名称、市名称、地区名称获取天气信息
    :param request: The request body containing province, city, and region
    :return: A JSON response containing the weather information
    """
    # 获取省份ID
    province_id = get_state(request.province)
    if not province_id:
        return {"error": "Province not found"}
    
    # 获取城市ID
    city_id = get_city(province_id, request.city)
    if not city_id:
        return {"error": "City not found"}
    
    # 获取区域ID
    region_id = get_region(province_id, city_id, request.region)
    if not region_id:
        return {"error": "Region not found"}
    
    # 获取天气数据
    weather_data = get_weather_sk(region_id)
    if not weather_data:
        return {"error": "Weather data not found"}
    
    return weather_data

# Endpoint to get weather information based on province, city, and region
@app.get(f"{WEATHER_BASE_URL}/cityinfo")
async def weather_sk(request: CityRequest) -> Dict[str, Any]:
    """
    根据输入的省名称、市名称、地区名称获取天气信息
    :param request: The request body containing province, city, and region
    :return: A JSON response containing the weather information
    """
    # 获取省份ID
    province_id = get_state(request.province)
    if not province_id:
        return {"error": "Province not found"}
    
    # 获取城市ID
    city_id = get_city(province_id, request.city)
    if not city_id:
        return {"error": "City not found"}
    
    # 获取区域ID
    region_id = get_region(province_id, city_id, request.region)
    if not region_id:
        return {"error": "Region not found"}
    
    # 获取天气数据
    weather_data = get_weather_cityinfo(region_id)
    if not weather_data:
        return {"error": "Weather data not found"}
    
    return weather_data

# Endpoint to get weather information based on province, city, and region
@app.get(f"{WEATHER_BASE_URL}/forecast")
async def weather_sk(request: CityRequest) -> Dict[str, Any]:
    """
    根据输入的省名称、市名称、地区名称获取天气信息
    :param request: The request body containing province, city, and region
    :return: A JSON response containing the weather information
    """
    # 获取省份ID
    province_id = get_state(request.province)
    if not province_id:
        return {"error": "Province not found"}
    
    # 获取城市ID
    city_id = get_city(province_id, request.city)
    if not city_id:
        return {"error": "City not found"}
    
    # 获取区域ID
    region_id = get_region(province_id, city_id, request.region)
    if not region_id:
        return {"error": "Region not found"}
    
    # 获取天气数据
    weather_data = get_weather_forecast(region_id)
    if not weather_data:
        return {"error": "Weather data not found"}
    
    return weather_data

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
