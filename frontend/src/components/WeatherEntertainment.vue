<template>
  <div class="weather-container" :style="{ backgroundImage: weatherData ? `url(${weatherBackground})` : '' }">
    <div class="weather-selector">
      <div>
        <label for="province">选择省份:</label>
        <select v-model="selectedProvince" @change="fetchCities">
          <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
        </select>
      </div>

      <div>
        <label for="city">选择城市:</label>
        <select v-model="selectedCity" @change="fetchRegions">
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <div>
        <label for="region">选择区域:</label>
        <select v-model="selectedRegion" @change="fetchWeatherData">
          <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">正在加载...</div>
    <div v-if="error" class="error">无法获取数据: {{ errorMessage }}</div>

    <div v-if="weatherData" class="weather-info">
      <h2>{{ weatherData.cityInfo.city }} - 实时天气</h2>
      <div class="current-weather">
        <div class="weather-details">
          <p class="temperature">{{ weatherData.data.wendu }}°C</p>
          <p class="humidity">湿度: {{ weatherData.data.shidu }}</p>
          <p class="air-quality">空气质量: {{ weatherData.data.quality }}</p>
          <p class="wind">风速: {{ weatherData.data.forecast[0].fx }} {{ weatherData.data.forecast[0].fl }}级</p>
        </div>
      </div>

      <h3>天气预报</h3>
      <ul>
        <li v-for="forecast in weatherData.data.forecast" :key="forecast.ymd" class="forecast-item">
          <span>{{ forecast.ymd }} - {{ forecast.type }} |</span> 温度: {{ forecast.high }} / {{ forecast.low }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

const provinces = ref<string[]>([]);
const cities = ref<string[]>([]);
const regions = ref<string[]>([]);
const selectedProvince = ref<string>('');
const selectedCity = ref<string>('');
const selectedRegion = ref<string>('');
const weatherData = ref<any>(null);
const weatherIcon = ref<string>('');  // 用于存储天气图标
const weatherBackground = ref<string>(''); // 用于存储背景图片
const loading = ref<boolean>(false); // 加载状态
const error = ref<boolean>(false); // 错误状态
const errorMessage = ref<string>(''); // 错误信息



const fetchProvinces = async () => {
  try {
    const response = await axios.get('http://localhost:8006/api/weather/province');
    provinces.value = response.data || [];
  } catch (error) {
    console.error('Failed to fetch provinces:', error);
  }
};

const fetchCities = async () => {
  try {
    if (selectedProvince.value) {
      const response = await axios.post('http://localhost:8006/api/weather/city', {
        province: selectedProvince.value
      });
      cities.value = response.data || [];
    }
  } catch (error) {
    console.error('Failed to fetch cities:', error);
  }
};

const fetchRegions = async () => {
  try {
    if (selectedProvince.value && selectedCity.value) {
      const response = await axios.post('http://localhost:8006/api/weather/region', {
        province: selectedProvince.value,
        city: selectedCity.value
      });
      regions.value = response.data || [];
    }
  } catch (error) {
    console.error('Failed to fetch regions:', error);
  }
};

const fetchWeatherData = async () => {
  loading.value = true;
  error.value = false;
  errorMessage.value = '';

  try {
    if (selectedRegion.value) {
      const response = await axios.post('http://localhost:8006/api/weather/code', {
        province: selectedProvince.value,
        city: selectedCity.value,
        region: selectedRegion.value
      });

      // 检查返回的 status 是否为 403，或者没有返回数据
      if (response.status === 403 || !response.data.id) {
        error.value = true;
        errorMessage.value = '该地区没有天气数据';
        loading.value = false;
        return;
      }

      const regionID = response.data.id;

      const weatherResponse = await axios.post('http://localhost:8006/api/weather/cityinfo', {
        regionID: regionID
      });

      // 检查天气数据是否为空
      if (!weatherResponse.data || !weatherResponse.data.data) {
        error.value = true;
        errorMessage.value = '无法获取该地区的天气数据';
        loading.value = false;
        return;
      }

      weatherData.value = weatherResponse.data;


      loading.value = false;  // 停止加载状态
    }
  } catch (error: any) {  // 或者 error: Error
    console.error('Failed to fetch weather data:', error);
    error.value = true;
    errorMessage.value = '发生错误，请稍后再试';
    loading.value = false;
  }
};

// 初始化时加载省份
onMounted(fetchProvinces);
</script>

<style scoped>
.weather-container {
  width: 70%; /* 保持宽度为 70% */
  max-height: 70vh; /* 最大高度为视口高度的 70% */
  margin: auto; /* 水平和垂直居中 */
  padding: 20px;
  background-size: cover;
  background-position: center;
  transition: background 1s ease;
  overflow-y: auto; /* 内容过长时可上下滚动 */
  display: flex;
  flex-direction: column; /* 使用 flexbox 垂直排列 */
  justify-content: flex-start; /* 修复为从顶部开始排列 */
  align-items: center; /* 水平居中内容 */
}

.weather-selector {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  width: 100%; /* 调整为占满父容器宽度 */
  z-index: 1; /* 确保选择器部分在最前面 */
}

.weather-selector label {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.weather-selector select {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  outline: none;
  transition: all 0.3s;
}

.weather-selector select:hover {
  border-color: #34495e;
}

.weather-info {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px; /* 为了与选择器区域有间距 */
  flex-grow: 1; /* 使天气信息部分可以自适应剩余空间 */
  width: 100%; /* 调整为占满父容器宽度 */
}


.current-weather {
  display: flex;
  align-items: center;
  gap: 20px;
}

.weather-icon {
  width: 60px;
  height: 60px;
}

.weather-details {
  font-size: 1.2rem;
}

.temperature {
  font-size: 2rem;
  font-weight: bold;
  color: #e74c3c;
}

.humidity,
.air-quality,
.wind {
  margin-top: 10px;
}

h3 {
  margin-top: 30px;
  font-size: 1.5rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

ul li {
  margin: 10px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.forecast-item span {
  font-weight: normal;
  color: #34495e;
}

.forecast-item {
  display: flex;
  justify-content: space-between;
}

.loading, .error {
  text-align: center;
  font-size: 1.2rem;
  color: #e74c3c;
}

</style>
