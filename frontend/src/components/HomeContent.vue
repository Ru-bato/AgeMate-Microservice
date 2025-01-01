<template>
    <div class="home-content">
      <SpeechToText @search="handleSearch" />
      <div v-if="searchResults.length > 0" class="search-results">
        <h2>搜索结果</h2>
        <ul>
          <li v-for="(result, index) in searchResults" :key="index">
            {{ result }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import SpeechToText from '@/components/SpeechToText.vue'
  import { ref } from 'vue'
  import axios from 'axios'
  
  const emit = defineEmits(['search'])
  
  const searchResults = ref<string[]>([])
  
  const handleSearch = async ({ query, url }: { query: string; url: string }) => {
    if (!query.trim() && !url.trim()) return
  
    try {
      // 假设有一个API端点用于搜索，支持query和url参数
      const response = await axios.get(`/api/search`, {
        params: {
          q: encodeURIComponent(query),
          url: encodeURIComponent(url),
        },
      })
      searchResults.value = response.data.results
    } catch (error) {
      console.error('搜索请求失败:', error)
      searchResults.value = ['未找到相关结果']
    }
  }
  </script>
  
  <style scoped>
  .home-content {
    /* 根据需要调整样式 */
    text-align: center;
  }
  
  .search-results {
    margin-top: 20px;
  }
  
  .search-results h2 {
    font-size: 2rem;
    margin-bottom: 10px;
  }
  
  .search-results ul {
    list-style-type: none;
    padding: 0;
  }
  
  .search-results li {
    background-color: #fff;
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  </style> 